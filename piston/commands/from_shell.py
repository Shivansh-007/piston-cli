import json
import random
from typing import List, Tuple

import requests
from piston.colorschemes import scheme_dict, schemes
from piston.utilities.compilers import languages_
from piston.utilities.constants import init_lexers, lexers_dict, Shell, spinners
from piston.utilities.prompt_continuation import prompt_continuation
from piston.utilities.utils import Utils
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls as sfpc
from pygments.styles import get_all_styles, get_style_by_name
from pygments.util import ClassNotFound
from rich.console import Console


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

    def set_language(self) -> None:
        """Prompt the user for the programming language, close program if language not supported."""
        language = self.console.input("Enter language: ", style="green").lower()

        if language not in languages_:
            self.console.print("Language is not supported!", style="bold red")
            Utils.close()

        self.language = language

    def get_args(self) -> List[str]:
        """Prompt the user for the command line arguments."""
        args = self.console.input(
            "Enter your args separated by comma: ", style="green"
        ).lower()
        return [x for x in args.strip().split(",") if x]

    def get_stdin(self) -> str:
        """Prompt the user for the standard input."""
        stdin = self.console.input(
            "Enter your stdin arguments: ", style="green"
        ).lower()
        return stdin

    def query_piston(self, code: str, args: List[str], stdin: str) -> dict:
        """Send a post request to the piston API with the code parameter."""
        output_json = {
            "language": self.language,
            "source": code,
            "args": args,
            "stdin": stdin,
        }

        with self.console.status("Compiling", spinner=random.choice(spinners)):
            return requests.post(
                "https://emkc.org/api/v1/piston/execute",
                data=json.dumps(output_json),
            ).json()

    def prompt_input(self) -> Tuple[str, str]:
        """Prompt the user for code input."""
        args = self.get_args()
        stdin = self.get_stdin()

        code = self.prompt_session.prompt(
            style=self.style,
        )

        if code.strip() == "exit":
            return "exit", self.language

        data = self.query_piston(code, args, stdin)

        if len(data["output"]) == 0:
            return "Your code ran without output.", self.language
        else:
            result = [
                f"{i:02d} | {line}"
                for i, line in enumerate(data["output"].split("\n"), 1)
            ]
            return "\n".join(result), self.language

    def run_shell(self, theme: str) -> None:
        """Run the shell."""
        self.set_language()
        self.set_prompt_session()
        self.set_style(theme)
        output = ""
        while output != "exit":
            output, language = self.prompt_input()
            if output != "exit":
                self.console.print(output)


from_shell = FromShell()
