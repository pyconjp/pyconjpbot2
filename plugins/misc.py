import random
from re import compile

from slack_bolt import App, BoltContext, Say


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
        say("pong", thread_ts=message.get("thread_ts"))
