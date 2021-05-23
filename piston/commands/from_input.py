from typing import Union

from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.shortcuts import prompt

from piston.utils import helpers, services
from piston.utils.constants import CONSOLE, PistonQuery
from piston.utils.lexers import lexers_dict


class FromInput:
    """Run code from input."""

    def ask_input(self, theme: str) -> Union[tuple, str]:
        """
        Make a multiline prompt for code input and send the code to the api.

        The compiled output from the api is returned.
        """
        language = helpers.get_lang()
        args = helpers.get_args()
        stdin = helpers.get_stdin()

        CONSOLE.print("[green]Enter your code, (press esc + enter to run)[/green]")
        style = helpers.set_style(theme)

        CONSOLE.print()
        code = prompt(
            "",
            lexer=PygmentsLexer(lexers_dict[language]),
            include_default_pygments_style=False,
            style=style,
            multiline=True,
        )
        payload = PistonQuery(language=language, args=args, stdin=stdin, code=code)

        data = services.query_piston(CONSOLE, payload)

        if len(data["output"]) == 0:
            return "Your code ran without output.", language

        return data["output"].split("\n"), language


FromInput = FromInput()
