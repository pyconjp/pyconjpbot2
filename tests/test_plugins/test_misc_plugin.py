"""
MiscPluginのユニットテスト

ping、shuffle、choiceコマンドの動作を検証するテスト
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.plugins.misc import MiscPlugin


class TestMiscPlugin:
    """MiscPluginのユニットテストクラス"""

    @pytest.fixture
    def plugin(self) -> MiscPlugin:
        """テスト用のMiscPluginインスタンスを作成"""
        plugin = MiscPlugin(MagicMock(), MagicMock(), MagicMock())
        return plugin

    @pytest.fixture
    def mock_message(self) -> MagicMock:
        """モックメッセージオブジェクトを作成"""
        msg = MagicMock()
        msg.say = AsyncMock()
        msg.sender.id = "U12345"
        msg.in_thread = False
        msg.ts = "1234567890.123456"
        return msg

    @pytest.mark.asyncio
    async def test_ping_command_returns_pong(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """pingコマンドが'pong'を返すことを検証"""
        await plugin.ping_command(mock_message)
        mock_message.say.assert_called_once_with("pong", thread_ts=None)

    @pytest.mark.asyncio
    async def test_ping_command_in_thread(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """スレッド内でpingコマンドが正しく動作することを検証"""
        mock_message.in_thread = True
        await plugin.ping_command(mock_message)
        # thread_tsパラメータが渡されることを確認
        call_args = mock_message.say.call_args
        assert "thread_ts" in call_args[1]
        assert call_args[1]["thread_ts"] == mock_message.ts

    @pytest.mark.asyncio
    async def test_ping_command_not_in_thread(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """スレッド外でpingコマンドが正しく動作することを検証"""
        mock_message.in_thread = False
        await plugin.ping_command(mock_message)
        # thread_tsがNoneであることを確認
        call_args = mock_message.say.call_args
        assert "thread_ts" in call_args[1]
        assert call_args[1]["thread_ts"] is None

    @pytest.mark.asyncio
    async def test_shuffle_command_with_words(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """shuffleコマンドが単語をシャッフルすることを検証"""
        words_str = "apple banana cherry"
        await plugin.shuffle_command(mock_message, words_str)
        # sayが呼ばれたことを確認
        assert mock_message.say.called
        # 呼び出された引数を取得
        call_args = mock_message.say.call_args
        shuffled_result = call_args[0][0]
        # シャッフルされた結果に元の単語がすべて含まれることを確認
        result_words = set(shuffled_result.split())
        expected_words = set(words_str.split())
        assert result_words == expected_words

    @pytest.mark.asyncio
    async def test_shuffle_command_without_words(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """shuffleコマンドが引数なしでヘルプメッセージを返すことを検証"""
        await plugin.shuffle_command(mock_message, None)
        expected_help = "使い方: `$shuffle <単語1> <単語2> ...`"
        mock_message.say.assert_called_once()
        call_args = mock_message.say.call_args
        assert expected_help in call_args[0][0]

    @pytest.mark.asyncio
    async def test_shuffle_command_with_empty_string(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """shuffleコマンドが空文字列でヘルプメッセージを返すことを検証"""
        await plugin.shuffle_command(mock_message, "")
        expected_help = "使い方: `$shuffle <単語1> <単語2> ...`"
        mock_message.say.assert_called_once()
        call_args = mock_message.say.call_args
        assert expected_help in call_args[0][0]

    @pytest.mark.asyncio
    async def test_shuffle_command_single_word(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """shuffleコマンドが1つの単語を正しく処理することを検証"""
        words_str = "apple"
        await plugin.shuffle_command(mock_message, words_str)
        call_args = mock_message.say.call_args
        shuffled_result = call_args[0][0]
        assert shuffled_result == "apple"

    @pytest.mark.asyncio
    async def test_choice_command_with_words(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """choiceコマンドが単語から1つ選択することを検証"""
        words_str = "apple banana cherry"
        await plugin.choice_command(mock_message, words_str)
        # sayが呼ばれたことを確認
        assert mock_message.say.called
        # 選択された結果が元の単語のいずれかであることを確認
        call_args = mock_message.say.call_args
        chosen_word = call_args[0][0]
        assert chosen_word in words_str.split()

    @pytest.mark.asyncio
    async def test_choice_command_without_words(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """choiceコマンドが引数なしでヘルプメッセージを返すことを検証"""
        await plugin.choice_command(mock_message, None)
        expected_help = "使い方: `$choice <単語1> <単語2> ...`"
        mock_message.say.assert_called_once()
        call_args = mock_message.say.call_args
        assert expected_help in call_args[0][0]

    @pytest.mark.asyncio
    async def test_choice_command_with_empty_string(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """choiceコマンドが空文字列でヘルプメッセージを返すことを検証"""
        await plugin.choice_command(mock_message, "")
        expected_help = "使い方: `$choice <単語1> <単語2> ...`"
        mock_message.say.assert_called_once()
        call_args = mock_message.say.call_args
        assert expected_help in call_args[0][0]

    @pytest.mark.asyncio
    async def test_choice_command_single_word(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """choiceコマンドが1つの単語を正しく処理することを検証"""
        words_str = "apple"
        await plugin.choice_command(mock_message, words_str)
        call_args = mock_message.say.call_args
        chosen_word = call_args[0][0]
        assert chosen_word == "apple"

    @pytest.mark.asyncio
    async def test_shuffle_command_in_thread(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """スレッド内でshuffleコマンドが正しく動作することを検証"""
        mock_message.in_thread = True
        words_str = "apple banana"
        await plugin.shuffle_command(mock_message, words_str)
        # thread_tsパラメータが渡されることを確認
        call_args = mock_message.say.call_args
        assert "thread_ts" in call_args[1]
        assert call_args[1]["thread_ts"] == mock_message.ts

    @pytest.mark.asyncio
    async def test_shuffle_command_not_in_thread(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """スレッド外でshuffleコマンドが正しく動作することを検証"""
        mock_message.in_thread = False
        words_str = "apple banana"
        await plugin.shuffle_command(mock_message, words_str)
        # thread_tsがNoneであることを確認
        call_args = mock_message.say.call_args
        assert "thread_ts" in call_args[1]
        assert call_args[1]["thread_ts"] is None

    @pytest.mark.asyncio
    async def test_choice_command_in_thread(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """スレッド内でchoiceコマンドが正しく動作することを検証"""
        mock_message.in_thread = True
        words_str = "apple banana"
        await plugin.choice_command(mock_message, words_str)
        # thread_tsパラメータが渡されることを確認
        call_args = mock_message.say.call_args
        assert "thread_ts" in call_args[1]
        assert call_args[1]["thread_ts"] == mock_message.ts

    @pytest.mark.asyncio
    async def test_choice_command_not_in_thread(
        self, plugin: MiscPlugin, mock_message: MagicMock
    ) -> None:
        """スレッド外でchoiceコマンドが正しく動作することを検証"""
        mock_message.in_thread = False
        words_str = "apple banana"
        await plugin.choice_command(mock_message, words_str)
        # thread_tsがNoneであることを確認
        call_args = mock_message.say.call_args
        assert "thread_ts" in call_args[1]
        assert call_args[1]["thread_ts"] is None
