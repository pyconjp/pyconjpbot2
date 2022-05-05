from slack_bolt import App

from .calc import enable_calc_plugin
from .greeting import enable_greeting_plugin
from .misc import enable_misc_plugin


def enable_plugins(app: App) -> None:
    enable_calc_plugin(app)
    enable_greeting_plugin(app)
    enable_misc_plugin(app)
