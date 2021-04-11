from typing import Tuple

from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles.pygments import style_from_pygments_cls as sfpc
from pygments.styles import get_all_styles, get_style_by_name
from pygments.util import ClassNotFound

from piston.colorschemes import scheme_dict, schemes
from piston.utils import helpers, services
from piston.utils.constants import CONSOLE, PistonQuery
from piston.utils.lexers import lexers_dict


class FromInput:
    """Run code from input."""

    def __init__(self) -> None:

        self.themes = list(get_all_styles()) + schemes

    def ask_input(self, theme: str = "solarized-dark") -> Tuple[str, str]:
        """
        Make a multiline prompt for code input and send the code to the api.

        The compiled output from the api is returned.
        """
        language = helpers.get_lang()
        args = helpers.get_args()
        stdin = helpers.get_stdin()

        CONSOLE.print("[green]Enter your code, (press esc + enter to run)[/green]")
        if theme in self.themes:
            try:
                style = sfpc(get_style_by_name(theme))
            except ClassNotFound:
                style = scheme_dict[theme]()
        else:
            CONSOLE.print(
                f"[red]Theme {theme} is not a valid theme, using piston-cli default.[/red]"
            )
            style = sfpc(get_style_by_name("solarized-dark"))

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

        result = [
            f"{i:02d} | {line}" for i, line in enumerate(data["output"].split("\n"), 1)
        ]
        return "\n".join(result), language


FromInput = FromInput()
