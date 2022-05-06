"""
Return a greeting message
"""

import random
from re import compile

from slack_bolt import App, Say


def _send_greeting(message: dict, say: Say, greetings: tuple[str, ...]) -> None:
    greeting = random.choice(greetings)
    say(f"<@{message['user']}> {greeting}", thread_ts=message.get("thread_ts"))


def enable_plugin(app: App) -> None:
    @app.message(compile(r"おはよう|お早う"))
    def morning(message: dict, say: Say) -> None:
        """Return morning greeting"""
        greetings = (
            "おはよう",
            "おはよー",
            "おはようございます",
        )
        _send_greeting(message, say, greetings)

    @app.message(compile(r"こんにち[はわ]"))
    def hello(message: dict, say: Say) -> None:
        """Return hello greeting"""
        greetings = (
            "こんにちは",
            "ちーっす",
            "こんにちは、元気ですかー?",
        )
        _send_greeting(message, say, greetings)

    @app.message(compile(r"いってきま|行ってきま"))
    def see_you(message: dict, say: Say) -> None:
        """Return see you greeting"""
        greetings = (
            "いってらっしゃい",
            "いってらっしゃーい",
            "いってらっしゃ～い",
            "いってら",
        )
        _send_greeting(message, say, greetings)

    @app.message(compile(r"眠た?い|ねむた?い|寝る|寝ます"))
    def night(message: dict, say: Say) -> None:
        """Return night greeting"""
        greetings = (
            "おやすみなさい",
            "おやす",
            "おやすー",
        )
        _send_greeting(message, say, greetings)
