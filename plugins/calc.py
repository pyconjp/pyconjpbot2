"""
Return a greeting message
"""

from re import compile

from slack_bolt import App, Say
from sympy import SympifyError, sympify

# single number pattern
NUM_PATTERN = compile(r"^\s*[-+]?[\d.,]+\s*$")


def enable_calc_plugin(app: App) -> None:
    @app.message(compile(r"^(([-+*/^%!(),.\d\s]|pi|e|sqrt|sin|cos|tan|log)+)$"))
    def calc(message: dict, say: Say) -> None:
        """
        Compute a string like a expression and return the result
        """
        expression = message["text"]
        expression = expression.replace(",", "")
        # ignore single number
        if NUM_PATTERN.match(expression):
            return

        try:
            result = sympify(expression)
        except SympifyError:
            # ignore not an expression
            return

        if result.is_Integer:
            answer = f"{int(result):,}"
        else:
            try:
                answer = f"{float(result):,}"
            except SympifyError:
                # ignore result is not a number
                return

        say(answer, thread_ts=message.get("thread_ts"))
