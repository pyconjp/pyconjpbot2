"""
Translate text
"""

import os
from re import compile

import deepl
from dotenv import load_dotenv
from slack_bolt import App, BoltContext, Say

# take environment variables from .env
load_dotenv()

HELP_TEXT = """
- `$translate python`: 指定した文字列を日本語に翻訳する
- `$translate へび`: 指定した文字列を英語に翻訳する
- `$translate -DE へび` : 指定した言語(DE等)に翻訳する
- `$translate list`: 指定できる言語の一覧を返す
"""

# Hiragana, Katakana, Kanji pattern
# https://note.nkmk.me/python-re-regex-character-type/
p = compile(
    r"[\u3041-\u309F\u30A1-\u30FF\uFF66-\uFF9F\u2E80-\u2FDF\u3005-\u3007"
    r"\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\U00020000-\U0002EBEF]"
)


def enable_plugin(app: App) -> None:
    @app.message(compile(r"^\$translate(\s+-([-\w]+))?\s+(.*)"))
    def wikipedia_command(message: dict, context: BoltContext, say: Say) -> None:
        """Translate text"""
        lang = context["matches"][1]  # target language
        text = context["matches"][2]

        if text == "help":
            say(HELP_TEXT, thread_ts=message.get("thread_ts"))
            return

        translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
        languages = [language.code for language in translator.get_languages()]

        if text == "list":
            language_list = " ".join(f"`{language}`" for language in languages)
            say(f"指定できる言語: {language_list}", thread_ts=message.get("thread_ts"))
            return

        if not lang:
            if p.match(text):
                lang = "EN-US"
            else:
                lang = "JA"
        elif lang.upper() not in languages:
            say(f"指定された言語 `{lang}` は存在しません", lang=lang)

        result = translator.translate_text(text, lang=lang)
        say(result.text, thread_ts=message.get("thread_ts"))
