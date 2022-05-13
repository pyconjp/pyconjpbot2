"""
add emoji reacion
"""

from re import IGNORECASE, compile

from slack_bolt import App
from slack_sdk import WebClient

# Reaction keywords and emoji
REACTION = {
    ("肉", "meat"): "meat_on_bone",
    ("ピザ", "pizza"): "pizza",
    ("sushi", "寿司", "おすし"): "sushi",
    ("酒",): "sake",
    ("ビール", "beer"): "beer",
    ("さくさく",): "panda_face",
    ("お茶",): "tea",
    ("コーヒー", "coffee"): "coffee",
    ("ケーキ",): "cake",
    ("ラーメン", "ramen"): "ramen",
}


def enable_plugin(app: App) -> None:
    keywords: list[str] = []
    for key in REACTION:
        keywords.extend(key)
    pattern = "|".join(keywords)

    @app.message(compile(pattern, IGNORECASE))
    def reaction(message: dict, client: WebClient) -> None:
        """add emoji reaction"""
        text = message["text"].lower()
        for words, emoji in REACTION.items():
            for word in words:
                if word in text:
                    # add emoji reaction
                    client.reactions_add(
                        channel=message["channel"],
                        timestamp=message["ts"],
                        name=emoji,
                    )
                    break
