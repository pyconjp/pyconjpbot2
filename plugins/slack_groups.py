import logging
from re import compile

from slack_bolt import App, BoltContext, Say
from slack_sdk import WebClient

from plugins.slack_utils import (
    get_display_name,
    get_user_id,
    list_usergroups,
    list_user_usergroups,
)

logger = logging.getLogger(__name__)


def enable_plugin(app: App) -> None:
    @app.message(compile(r"^\$slack-groups\s+list$"))
    def slack_groups_list(client: WebClient, message: dict, say: Say) -> None:
        """
        Returns list of user groups
        """
        logger.info("execute slack_groups_list function")
        groups = [
            f"- `{handle}`: {g['name']} {g['description']}"
            for handle, g in list_usergroups(client).items()
        ]
        msg = "\n".join(groups)
        say(msg, thread_ts=message.get("thread_ts"))
        return None

    @app.message(compile(r"^\$slack-groups\s+members\s+(\S+)$"))
    def slack_group_members(
        client: WebClient, message: dict, context: BoltContext, say: Say
    ) -> None:
        """
        Returns list of users in groups

        $slack-groups members riji
        """
        logger.info("execute slack_group_members function")
        groups = list_usergroups(client)
        keyword: str = context["matches"][0]

        if keyword not in groups:
            logger.warning("not found for %s group", keyword)
            msg = f"グループ{keyword}が見つかりませんでした"
            say(msg, thread_ts=message.get("thread_ts"))
            return None

        gid = groups[keyword].get("id")

        user_ids = list_user_usergroups(client, gid)
        users = [get_display_name(client, u) for u in user_ids]

        msg = f"グループ {keyword} のユーザー({len(users)}人): " + ", ".join(users)
        say(msg, thread_ts=message.get("thread_ts"))

    @app.message(compile(r"^\$slack-groups\s+member\s+add\s+(\S+)\s+(\S+)$"))
    def slack_group_add_user(
        client: WebClient, message: dict, context: BoltContext, say: Say
    ):
        logger.info("execute slack_group_add_user function")
        groups = list_usergroups(client)
        keyword: str = context["matches"][0]
        target_users: list[str] = context["matches"][1].split(" ")

        if keyword not in groups:
            logger.warning("not found for %s group", keyword)
            msg = f"グループ{keyword}が見つかりませんでした"
            say(msg, thread_ts=message.get("thread_ts"))
            return None

        gid = groups[keyword].get("id")
        existing = list_user_usergroups(client, gid)
        user_ids = [get_user_id(client, u) for u in target_users]
        if not user_ids or None in user_ids:
            logger.warning("target user id not found....")
            msg = f"指定されたユーザー({' '.join(target_users)})はありませんでした"
            say(msg, thread_ts=message.get("thread_ts"))
            return None

        target = existing + user_ids
        result = client.usergroups_users_update(usergroup=gid, users=target)
        logger.debug("Updated Group: %s", result.data)
        msg = f"グループ{keyword}にユーザー{', '.join(target_users)}を追加しました"
        say(msg)
        return None
