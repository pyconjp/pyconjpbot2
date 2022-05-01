import logging
import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# take environment variables from .env
load_dotenv()

logging.basicConfig(level=logging.DEBUG)

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
