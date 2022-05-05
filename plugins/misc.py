import random
from re import compile

from slack_bolt import App, BoltContext, Say
from slack_sdk import WebClient

from .slack_utils import get_display_name, get_user_ids


def enable_misc_plugin(app: App) -> None:
    @app.message(compile(r"^\$choice\s+(.*)"))
    def choice(message: dict, say: Say, context: BoltContext) -> None:
        """choice and return one of the specified keywords"""

        choiced = ""
        words = context["matches"][0].split()

        if len(words) == 1:
            choiced = random.choice(words[0])
        else:
            choiced = random.choice(words)
        say(choiced, thread_ts=message.get("thread_ts"))

    @app.message(compile(r"^\$shuffle\s+(.*)"))
    def shuffle(message: dict, say: Say, context: BoltContext) -> None:
        """Shuffle and return specified keywords"""
        words = context["matches"][0].split()
        if len(words) == 1:
            words = list(words[0])

        random.shuffle(words)
        say(" ".join(words), thread_ts=message.get("thread_ts"))

    @app.message(compile(r"^\$ping$"))
    def ping(message: dict, say: Say) -> None:
        """return pong in response to ping"""
        breakpoint()
        say("pong", thread_ts=message.get("thread_ts"))

    @app.message(compile(r"^\$random(\s+(active|help))?$"))
    def random_command(
        client: WebClient, message: dict, say: Say, context: BoltContext
    ) -> None:
        """
        Return one member at random from the members in the channel

        - https://api.slack.com/methods/conversations.members
        - https://api.slack.com/methods/users.getPresence
        - https://api.slack.com/methods/users.info
        """

        subcommand = context["matches"][1]
        if subcommand == "help":
            say(
                """
- `$random`: チャンネルにいるメンバーからランダムに一人を選ぶ
- `$random active`: チャンネルにいるactiveなメンバーからランダムに一人を選ぶ
""",
                mrkdwn=True,
                thread_ts=message.get("thread_ts"),
            )
            return

        # get channel members
        results = client.conversations_members(channel=message["channel"])
        members = results["members"]

        # get member ids without bot user
        user_ids = list(set(members) & set(get_user_ids(client)))

        if subcommand == "active":
            random.shuffle(user_ids)
            for user_id in user_ids:
                presence = client.users_getPresence(user=user_id)
                if presence["precense"] != "active":
                    break
        else:
            user_id = random.choice(user_ids)

        name = get_display_name(client, user_id)
        say(f"{name} さん、君に決めた！", thread_ts=message.get("thread_ts"))
