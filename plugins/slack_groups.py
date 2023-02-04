import logging
from re import compile

from slack_bolt import App, BoltContext, Say
from slack_sdk import WebClient

from plugins.slack_utils import get_display_name, _list_usergroups

logger = logging.getLogger(__name__)


def enable_plugin(app: App) -> None:
    @app.message(compile(r"^\$slack-groups\s+list$"))
    def slack_groups_list(client: WebClient, message: dict, say: Say) -> None:
        """
        Returns list of user groups
        """
        logger.info("execute slack_groups_list function")
        groups = [
            f"- `{handle}`: {g['name']} ({g['description']})"
            for handle, g in _list_usergroups(client).items()
        ]
        msg = "\n".join(groups)
        say(msg, thread_ts=message.get("thread_ts"))
        return None
