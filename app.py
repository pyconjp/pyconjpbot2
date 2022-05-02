import logging
import os
from typing import Any

from dotenv import load_dotenv
from slack_bolt import App, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler

from plugins import enable_plugins

# take environment variables from .env
load_dotenv()

logging.basicConfig(level=logging.DEBUG)

# Initializes app with bot token
app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.message("hello")
def message_hello(message: dict[str, Any], say: Say) -> None:
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")


enable_plugins(app)


# Start pycon jp bot
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
