from slack_bolt import App

from .misc import enable_misc_plugin


def enable_plugins(app: App) -> None:
    enable_misc_plugin(app)
