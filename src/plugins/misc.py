"""基本的なボットコマンド（misc）プラグイン

User Story 1: ping, shuffle, choiceコマンドを提供
"""

import random

from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import respond_to
from machine.plugins.message import Message
from structlog.stdlib import get_logger

from .utils import get_thread_ts

logger = get_logger(__name__)


class MiscPlugin(MachineBasePlugin):
    """基本的なユーティリティコマンドを提供するプラグイン"""

    @respond_to(r"^ping$")
    async def ping_command(self, msg: Message) -> None:
        """ボットの動作確認コマンド

        コマンド: $ping
        応答: pong
        """
        logger.info(f"ping_command: user={msg.sender.id}")
        await msg.say("pong", thread_ts=get_thread_ts(msg))

    @respond_to(r"^shuffle(\s+(?P<words_str>.*)|\s*)$")
    async def shuffle_command(self, msg: Message, words_str: str | None) -> None:
        """shuffle: 単語をシャッフルするコマンド

        コマンド: $shuffle <単語1> <単語2> ...
        応答: シャッフルされた単語のリスト
        """
        logger.info(f"shuffle_command: user={msg.sender.id}, input={words_str}")

        help_text = "使い方: `$shuffle <単語1> <単語2> ...`"
        resp_msg = help_text
        if words_str is not None:
            words = words_str.split()
            if words:
                random.shuffle(words)
                result = " ".join(words)
                logger.info(f"shuffle_command: result={result}")
                resp_msg = result

        await msg.say(resp_msg, thread_ts=get_thread_ts(msg))

    @respond_to(r"^choice(\s+(?P<words_str>.*)|\s*)$")
    async def choice_command(self, msg: Message, words_str: str | None) -> None:
        """choice: 単語からランダムに1つ選択するコマンド

        コマンド: $choice <単語1> <単語2> ...
        応答: ランダムに選ばれた1つの単語
        """
        logger.info(f"choice_command: user={msg.sender.id}, input={words_str}")

        help_text = "使い方: `$choice <単語1> <単語2> ...`"
        resp_msg = help_text
        if words_str is not None:
            words = words_str.split()
            if words:
                result = random.choice(words)
                logger.info(f"choice_command: result={result}")
                resp_msg = f"{result}"

        await msg.say(resp_msg, thread_ts=get_thread_ts(msg))
