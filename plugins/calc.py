"""
Calculate formulas
"""

import logging
from re import compile

from slack_bolt import App, Say
from sympy import SympifyError, sympify

# single number pattern
NUM_PATTERN = compile(r"^\s*[-+]?[\d.,]+\s*$")

logger = logging.getLogger(__name__)


def enable_plugin(app: App) -> None:
    @app.message(compile(r"^(([-+*/^%!(),.\d\s]|pi|e|sqrt|sin|cos|tan|log)+)$"))
    def calc(message: dict, say: Say) -> None:
        """
        Calculate a string like a formula and return the result
        """
        logger.info("excecute calc function")
        formula = message["text"]
        formula = formula.replace(",", "")
        # ignore single number
        if NUM_PATTERN.match(formula):
            return

        try:
            result = sympify(formula)
        except SympifyError:
            # ignore not a formula
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
