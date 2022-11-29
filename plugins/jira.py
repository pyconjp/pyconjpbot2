"""
jira
"""

import logging
import os
from re import compile

from dotenv import load_dotenv
from jira import JIRA, JIRAError
from slack_bolt import App, Say
from slack_sdk.models.blocks import SectionBlock

# take environment variables from .env
load_dotenv()

# Clean JIRA Url to not have trailing / if exists
CLEAN_JIRA_URL = os.environ["JIRA_URL"].removesuffix("/")

# Login to jira
jira_auth = (os.environ["JIRA_USER"], os.environ["JIRA_TOKEN"])
jira = JIRA(CLEAN_JIRA_URL, basic_auth=jira_auth)

projects = jira.projects()
project_keys = [prj.key for prj in projects]
issue_pattern = compile(rf"({'|'.join(project_keys)})-\d+")

logger = logging.getLogger(__name__)


def _create_issue_blocks(issue_id: str) -> list[SectionBlock]:
    """Create blocks for issue information"""
    issue = jira.issue(issue_id)

    summary = issue.fields.summary
    if issue.fields.assignee:
        assignee = issue.fields.assignee.displayName
    else:
        assignee = "未割り当て"
    status = issue.fields.status.name
    issue_url = issue.permalink()

    blocks = [
        SectionBlock(
            text=f"*<{issue_url}|{issue_id} {summary}>*",
            fields=[f"担当者: {assignee}", f"ステータス: {status}"],
        ),
    ]
    return blocks


def enable_plugin(app: App) -> None:
    @app.message(issue_pattern)
    def jira_issue(message: dict, say: Say) -> None:
        """Return issue information"""
        logger.info("execute jira_issue function")
        # find all issue id in message
        for m in issue_pattern.finditer(message["text"]):
            try:
                blocks = _create_issue_blocks(m[0])
                say(blocks=blocks, thread_ts=message.get("thread_ts"))
            except JIRAError:
                pass
