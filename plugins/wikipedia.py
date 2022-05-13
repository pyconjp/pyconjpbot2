"""
Return Wikipedia page for specified keywords and language
"""

from re import compile

import wikipedia
from slack_bolt import App, BoltContext, Say


def _wikipedia_command(lang: str, query: str) -> str:
    if query == "help":
        return """
- `$wikipedia keywords`: Wikipediaで指定されたキーワードに関連するページを返す
- `$wikipedia -en keywords`: Wikipediaで指定された言語(en等)のページを返す
"""

    if not lang:
        lang = "ja"
    elif lang not in wikipedia.language():
        # invalid language
        return f"指定された言語 `{lang}` は存在しません"

    wikipedia.set_lang(lang)

    # search with query
    results = wikipedia.search(query, results=1)
    if results:
        page = wikipedia.page(results[0])
        return f"Wikipedia: <{page.url}|{page.title}>"
    else:
        # page not found
        return f"`{query}` に該当するページはありません"


def enable_plugin(app: App) -> None:
    @app.message(compile(r"^\$wikipedia(\s+-(\w+))?\s+(.*)$"))
    def wikipedia_command(message: dict, context: BoltContext, say: Say) -> None:
        """Return Wikipedia page for specified keywords and language"""
        lang = context["matches"][1]
        query = context["matches"][2]

        result = _wikipedia_command(lang, query)
        say(result, thread_ts=message.get("thread_ts"))
