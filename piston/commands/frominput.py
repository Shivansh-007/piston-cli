import json
import random
from typing import List

import requests
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles.pygments import style_from_pygments_cls as sfpc
from pygments.styles import get_all_styles, get_style_by_name
from pygments.util import ClassNotFound
from piston.colorschemes import scheme_dict, schemes
from piston.utilities.compilers import languages_
from piston.utilities.constants import init_lexers, lexers_dict, spinners
from piston.utilities.utils import Utils
from rich.console import Console


class FromInput:
    """Run code from input."""

    def __init__(self) -> None:
        init_lexers()
        self.languages = languages_

        self.console = Console()
        self.output_json = dict()
        self.spinners = spinners
        self.themes = list(get_all_styles()) + schemes

    def get_lang(self) -> str:
        """Prompt the user for the programming language, close program if language not supported."""
        language = self.console.input("[green]Enter language:[/green] ").lower()

        if language not in self.languages:
            self.console.print("Language is not supported!", style="bold red")
            Utils.close()
        return language

    def get_args(self) -> List[str]:
        """Prompt the user for the command line arguments."""
        args = self.console.input(
            "[green]Enter your args separated by comma:[/green] "
        ).lower()
        return [x for x in args.strip().split(",") if x]

    def get_stdin(self) -> str:
        """Prompt the user for the standard input."""
        stdin = self.console.input(
            "[green]Enter your stdin arguments:[/green] "
        ).lower()
        return stdin

    def askinp(self, theme: str = "solarized-dark") -> str:
        """
        Make a multiline prompt for code input and send the code to the api.

        The compiled output from the api is returned.
        """
        language = self.get_lang()
        args = self.get_args()
        stdin = self.get_stdin()

        self.console.print(
            "Enter your code, (press esc + enter to run)\n", style="green"
        )
        if theme in self.themes:
            try:
                style = sfpc(get_style_by_name(theme))
            except ClassNotFound:
                style = scheme_dict[theme]()
        else:
            style = sfpc(get_style_by_name("solarized-dark"))

        code = prompt(
            "",
            lexer=PygmentsLexer(lexers_dict[language]),
            include_default_pygments_style=False,
            style=style,
            multiline=True,
        )

        self.output_json = {
            "language": language,
            "source": code,
            "args": args,
            "stdin": stdin,
        }

        with self.console.status("Compiling", spinner=random.choice(self.spinners)):
            data = requests.post(
                "https://emkc.org/api/v1/piston/execute",
                data=json.dumps(self.output_json),
            ).json()

        if len(data["output"]) == 0:
            return "Your code ran without output."
        else:
            result = [
                f"{i:02d} | {line}"
                for i, line in enumerate(data["output"].split("\n"), 1)
            ]
            return "\n".join(result)


FromInput = FromInput()
