import json
import random
from dataclasses import dataclass
from typing import List

import requests
from piston.colorschemes import scheme_dict, schemes
from piston.utilities.compilers import languages_
from piston.utilities.constants import Shell, init_lexers, lexers_dict, spinners
from piston.utilities.prompt_continuation import prompt_continuation
from piston.utilities.utils import Utils
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls as sfpc
from pygments.styles import get_all_styles, get_style_by_name
from pygments.util import ClassNotFound
from rich.console import Console


@dataclass
class PistonQuery:
    """Represents the payload sent to the Piston API."""

    code: str
    args: List[str]
    stdin: str


class FromShell:
    """Run code from a shell environment."""

    def __init__(self):
        init_lexers()

        self.console = Console()
        self.themes = list(get_all_styles()) + schemes
        self.style = None
        self.language = None
        self.prompt_session = None

    def set_prompt_session(self) -> None:
        """Set the prompt session to use for input."""
        self.prompt_session = PromptSession(
            Shell.promp_start,
            include_default_pygments_style=False,
            lexer=PygmentsLexer(lexers_dict[self.language]),
            multiline=True,
            prompt_continuation=prompt_continuation,
        )

    def set_style(self, theme: str) -> None:
        """Set the theme for prompt_toolkit."""
        if theme in self.themes:
            try:
                self.style = sfpc(get_style_by_name(theme))
            except ClassNotFound:
                self.style = scheme_dict[theme]()
        else:
            self.style = sfpc(get_style_by_name("solarized-dark"))

    def set_language(self, language: str) -> None:
        """Prompt the user for the programming language, close program if language not supported."""
        if language not in languages_:
            self.console.print("[bold red]Language is not supported![/bold red]")
            Utils.close()

        self.language = language

    def get_args(self) -> List[str]:
        """Prompt the user for the command line arguments."""
        args = self.console.input("[green]Enter your args separated by comma:[/green] ")
        return [x for x in args.strip().split(",") if x]

    def get_stdin(self) -> str:
        """Prompt the user for the standard input."""
        stdin = self.console.input(
            "[green]Enter your stdin arguments by comma:[/green] "
        )
        return "\n".join([x for x in stdin.strip().split(",") if x])

    def query_piston(self, payload: PistonQuery) -> dict:
        """Send a post request to the piston API with the code parameter."""
        output_json = {
            "language": self.language,
            "source": payload.code,
            "args": payload.args,
            "stdin": payload.stdin,
        }

        with self.console.status("Compiling", spinner=random.choice(spinners)):
            return requests.post(
                "https://emkc.org/api/v1/piston/execute",
                data=json.dumps(output_json),
            ).json()

    def prompt(self) -> PistonQuery:
        """Prompt the user for code input."""
        code = self.prompt_session.prompt(
            style=self.style,
        )

        args = self.get_args()
        stdin = self.get_stdin()

        return PistonQuery(
            code=code,
            args=args,
            stdin=stdin,
        )

    def run_shell(self, language: str, theme: str) -> None:
        """Run the shell."""
        self.console.print(
            "[bold blue]NOTE: stdin and args will be prompted after code. "
            "Use escape + enter to finish writing the code. "
            "To quit, use ctrl + c. [/bold blue]"
        )

        self.set_language(language)
        self.set_prompt_session()
        self.set_style(theme)

        while True:
            query = self.prompt()

            data = self.query_piston(query)

            if len(data["output"]) == 0:
                self.console.print("Your code ran without output.")
            else:
                self.console.print(
                    "\n".join(
                        [
                            f"{i:02d} | {line}"
                            for i, line in enumerate(data["output"].split("\n"), 1)
                        ]
                    )
                )


from_shell = FromShell()
