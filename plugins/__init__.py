from slack_bolt import App

from . import calc, greeting, misc, wikipedia


def enable_plugins(app: App) -> None:
    calc.enable_plugin(app)
    greeting.enable_plugin(app)
    misc.enable_plugin(app)
    wikipedia.enable_plugin(app)
