"""
プラグインで汎用的に使用する関数やクラスを定義するモジュール
"""

from machine.plugins.message import Message


def get_thread_ts(msg: Message) -> str | None:
    """
    メッセージがスレッドの中の場合はスレッドのタイムスタンプを返す。スレッドの中じゃない場合はNoneを返す。

    Args:
        msg (Message): メッセージオブジェクト

    Returns:
        str | None: スレッドタイムスタンプまたはNone
    """
    return msg.ts if msg.in_thread else None
