"""
Plusplus
"""

import random
from re import compile

from slack_bolt import App, BoltContext, Say
from slack_sdk import WebClient

from .plusplus_model import Plusplus
from .slack_utils import get_display_name

HELP_TEXT = """
- `name1 name2++`: 指定された名前に +1 カウントする
- `name1 name2--`: 指定された名前に -1 カウントする
- `$plusplus search (keyword)`: 名前にkeywordを含む一覧を返す
- `$plusplus delete (name)`: 指定されたnameのカウントを削除する(カウント10未満のみ)
- `$plusplus rename (before) (after)`: カウントする名前をafterに変更する
- `$plusplus merge (source) (target)`: 2つの名前のカウントをtargetにまとめる
"""

PLUS_MESSAGE = (
    "leveled up!",
    "レベルが上がりました!",
    "やったね",
    "(☝՞ਊ ՞)☝ウェーイ",
)

MINUS_MESSAGE = (
    "leveled down.",
    "レベルが下がりました",
    "ドンマイ!",
    "(´・ω・｀)",
)


def _update_count(target: str, is_plus: bool) -> int:
    """
    Update plusplus count

    :param target: target name
    :param is_plus: True: increment / False: decrement
    """
    target = target.lower()
    plus, created = Plusplus.get_or_create(name=target, defaults={"counter": 0})

    if is_plus:
        plus.counter += 1
    else:
        plus.counter -= 1
    plus.save()
    return plus.counter


def enable_plugin(app: App) -> None:
    @app.message(compile(r"^(.*[^+-]):?\s*([+-]{2,})"))
    def multi_plusplus(
        message: dict, client: WebClient, context: BoltContext, say: Say
    ) -> None:
        """
        ++ (or --) for multiple names given

        Example:
        takanory++
        takanory terada++
        @takanory++
        takanory  --
        """
        targets = context["matches"][0].split()

        plus_or_minus = context["matches"][1]
        # ignore --- or +++
        if len(plus_or_minus) > 2:
            return
        is_plus = plus_or_minus == "++"

        for target in targets:
            # convert user_id(<@XXXXXX>) to user_name
            if target.startswith("<@"):
                user_id = target[2:-1]  # user_idを取り出す
                target = get_display_name(client, user_id)
            # remove '@' prefix
            target = target.removeprefix("@")

            # ignore 1 character target
            if len(target) < 2:
                continue

            # plus or minus counter
            counter = _update_count(target, is_plus)
            if is_plus:
                msg = random.choice(PLUS_MESSAGE)
            else:
                msg = random.choice(MINUS_MESSAGE)
            say(f"{target} {msg} (通算: {counter})", thread_ts=message.get("thread_ts"))

    @app.message(compile(r"^\$plusplus\s+help"))
    def plusplus_help(message: dict, say: Say) -> None:
        """
        Send a help message
        """
        say(HELP_TEXT, thread_ts=message.get("thread_ts"))
