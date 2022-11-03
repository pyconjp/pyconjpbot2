"""
Count ++ for a given name
"""

import logging
import random
from re import compile

from peewee import IntegrityError
from slack_bolt import App, BoltContext, Say
from slack_sdk import WebClient

from .plusplus_model import Plusplus
from .slack_utils import get_display_name

HELP_TEXT = """
- `name1 name2++`: 指定された名前に +1 カウントする
- `name1 name2--`: 指定された名前に -1 カウントする
- `$plusplus search (keyword)`: 名前にkeywordを含む一覧を返す
- `$plusplus delete (name)`: 指定されたnameのカウントを削除する(カウント10未満のみ)
- `$plusplus rename (old) (new)`: カウントする名前をnewに変更する
- `$plusplus merge (old) (new)`: 2つの名前のカウントをnewにまとめ、oldを削除する
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

logger = logging.getLogger(__name__)


def _update_count(name: str, is_plus: bool) -> int:
    """
    Update plusplus count

    :param name: target name
    :param is_plus: True: increment / False: decrement
    """
    plus, created = Plusplus.get_or_create(name=name.lower(), defaults={"counter": 0})

    if is_plus:
        plus.counter += 1
    else:
        plus.counter -= 1
    plus.save()
    return plus.counter


def _plusplus_delete(name: str) -> str:
    """
    Delete counter

    :param name: name of counter
    :return: message
    """
    # get instance
    try:
        plus = Plusplus.get(Plusplus.name == name)
    except Plusplus.DoesNotExist:
        return f"`{name}` という名前は登録されていません"

    if abs(plus.counter) >= 10:
        return f"`{name}` のカウントが多いので削除を取り消しました(count: {plus.counter})"

    plus.delete_instance()
    return f"`{name}` を削除しました"


def _plusplus_rename(old_name: str, new_name: str) -> str:
    """
    Rename old name to new name

    :param old_name: old name
    :param new_name: new name
    :return: message
    """

    if old_name == new_name:
        return "変更前後では異なる名前を指定してください"

    # get instance of old name
    try:
        old = Plusplus.get(Plusplus.name == old_name)
    except Plusplus.DoesNotExist:
        return f"`{old_name}` という名前は登録されていません"

    try:
        # create instance of new name
        new = Plusplus.create(name=new_name, counter=old.counter)
    except IntegrityError:
        return f"`{new_name}` という名前はすでに登録されています"

    # delete old instance
    old.delete_instance()
    return f"`{old_name}` から `{new_name}` に名前を変更しました(count: {new.counter})"


def _plusplus_merge(old_name: str, new_name: str) -> str:
    """
    Mewrge counts of old name and new name into new and delete old

    :param old_name: old name
    :param new_name: new name
    :return: message
    """
    try:
        old = Plusplus.get(name=old_name)
    except Plusplus.DoesNotExist:
        return f"`{old_name}` という名前は登録されていません"

    try:
        new = Plusplus.get(name=new_name)
    except Plusplus.DoesNotExist:
        return f"`{new_name}` という名前は登録されていません"

    message = (
        f"`{old_name}` を `{new_name}` に統合しました"
        f"(count: {old.counter} + {new.counter} = {old.counter + new.counter})"
    )
    # merge counts and delete old
    new.counter += old.counter
    new.save()
    old.delete_instance()

    return message


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
        logger.info("executge multi_plusplus function")
        targets = context["matches"][0].split()

        plus_or_minus = context["matches"][1]
        # ignore --- or +++
        if len(plus_or_minus) > 2:
            return
        is_plus = plus_or_minus == "++"

        for target in targets:
            # convert user_id(<@XXXXXX>) to user_name
            if target.startswith("<@"):
                user_id = target[2:-1]
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

    @app.message(compile(r"^\$plusplus\s+search\s+(\S+)"))
    def plusplus_search(message: dict, context: BoltContext, say: Say) -> None:
        """
        Return names and counts containing the keyword

        $plusplus search taka
        """
        logger.info("executge plusplus_search function")
        keyword = context["matches"][0]
        pattern = f"%{keyword}%"
        pluses = Plusplus.select().where(Plusplus.name**pattern)

        if len(pluses) == 0:
            msg = f"`{keyword}` を含む名前はありません"
        else:
            msg = f"`{keyword}` を含む名前とカウントの一覧\n"
            for plus in pluses:
                msg += f"- {plus.name}(count: {plus.counter})\n"

        say(msg, thread_ts=message.get("thread_ts"))

    @app.message(r"^\$plusplus\s+delete\s+(\S+)")
    def plusplus_delete(message: dict, context: BoltContext, say: Say) -> None:
        """
        Delete counts for a given name. Counts only less than 10

        $plusplus delete takanory
        """
        logger.info("executge plusplus_delete function")
        name = context["matches"][0]
        msg = _plusplus_delete(name)
        say(msg, thread_ts=message.get("thread_ts"))

    @app.message(r"^\$plusplus\s+rename\s+(\S+)\s+(\S+)")
    def plusplus_rename(message: dict, context: BoltContext, say: Say) -> None:
        """
        Rename old name to new name

        $plusplus rename (old) (new)
        """

        old = context["matches"][0]
        new = context["matches"][1]
        msg = _plusplus_rename(old, new)
        say(msg, thread_ts=message.get("thread_ts"))

    @app.message(r"^\$plusplus\s+merge\s+(\S+)\s+(\S+)")
    def plusplus_merge(message: dict, context: BoltContext, say: Say) -> None:
        """
        Merge counts of old name and new name into new and delete old

        $plusplus merge (old) (new)
        """
        logger.info("executge plusplus_merge function")

        old = context["matches"][0]
        new = context["matches"][1]
        msg = _plusplus_merge(old, new)
        say(msg, thread_ts=message.get("thread_ts"))

    @app.message(compile(r"^\$plusplus\s+help"))
    def plusplus_help(message: dict, say: Say) -> None:
        """
        Send a help message
        """
        logger.info("executge plusplus_help function")
        say(HELP_TEXT, thread_ts=message.get("thread_ts"))
