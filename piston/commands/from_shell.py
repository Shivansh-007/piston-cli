from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer

from piston.utils import helpers, services
from piston.utils.compilers import languages_
from piston.utils.constants import CONSOLE, PistonQuery, Shell
from piston.utils.lexers import lexers_dict
from piston.utils.prompt_continuation import prompt_continuation


class FromShell:
    """Run code from a shell environment."""

    def __init__(self):
        self.style = None
        self.language = None
        self.prompt_session = None

    def set_prompt_session(self) -> None:
        """Set the prompt session to use for input."""
        self.prompt_session = PromptSession(
            Shell.prompt_start,
            include_default_pygments_style=False,
            lexer=PygmentsLexer(lexers_dict[self.language]),
            multiline=True,
            prompt_continuation=prompt_continuation,
        )

    def set_language(self, language: str) -> None:
        """
        Set the language to the option passed by use.

        If language is not supported then exit the CLI.
        """
        if language not in languages_:
            CONSOLE.print("[bold red]Language is not supported![/bold red]")
            helpers.close()

        self.language = language

    def prompt(self) -> PistonQuery:
        """Prompt the user for code input."""
        code = self.prompt_session.prompt(
            style=self.style,
        )

        args = helpers.get_args()
        stdin = helpers.get_stdin()

        return PistonQuery(
            language=self.language,
            code=code,
            args=args,
            stdin=stdin,
        )

    def run_shell(self, language: str, theme: str) -> None:
        """Run the shell."""
        CONSOLE.print(
            "[bold blue]NOTE: stdin and args will be prompted after code. "
            "Use escape + enter to finish writing the code. "
            "To quit, use ctrl + c. [/bold blue]"
        )

        self.set_language(language)
        self.set_prompt_session()
        self.style = helpers.set_style(theme)

        while True:
            query = self.prompt()

            data = services.query_piston(CONSOLE, query)

            if len(data["output"]) == 0:
                CONSOLE.print("Your code ran without output.")
            else:
                CONSOLE.print(
                    "\n".join(
                        [
                            f"{i:02d} | {line}"
                            for i, line in enumerate(data["output"].split("\n"), 1)
                        ]
                    )
                )


from_shell = FromShell()
