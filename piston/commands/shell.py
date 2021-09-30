import click
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer

from piston.utils import helpers, services
from piston.utils.compilers import languages_
from piston.utils.constants import PistonQuery
from piston.utils.lexers import lexers_dict


class Shell:
    """Run code from a shell environment."""

    def __init__(self, ctx: click.Context):
        self.ctx = ctx
        self.console = ctx.obj["console"]
        self.style = None
        self.language = None
        self.prompt_session = None

    def set_prompt_session(self, prompt_start: str, prompt_continuation: str) -> None:
        """Set the prompt session to use for input."""
        self.prompt_session = PromptSession(
            prompt_start,
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
            self.console.print("[bold red]Language is not supported![/bold red]")
            self.ctx.exit()

        self.language = language

    def prompt(self) -> PistonQuery:
        """Prompt the user for code input."""
        code = self.prompt_session.prompt(
            style=self.style,
        )

        args = helpers.get_args(self.console)
        stdin = helpers.get_stdin(self.console)

        return PistonQuery(
            language=self.language,
            code=code,
            args=args,
            stdin=stdin,
        )

    def run_shell(self, language: str, theme: str, prompt_start: str, prompt_continuation: str) -> None:
        """Run the shell."""
        self.console.print(
            "[bold blue]NOTE: stdin and args will be prompted after code. "
            "Use escape + enter to finish writing the code. "
            "To quit, use ctrl + c. [/bold blue]"
        )

        self.set_language(language)
        self.set_prompt_session(prompt_start, prompt_continuation)
        self.style = helpers.set_style(self.console, theme)

        while True:
            query = self.prompt()
            data = services.query_piston(self.ctx, self.console, query)

            if len(data["output"]) == 0:
                self.console.print("Your code ran without output.")
            else:
                self.console.print(
                    "\n".join([f"{i:02d} | {line}" for i, line in enumerate(data["output"].split("\n"), 1)])
                )
