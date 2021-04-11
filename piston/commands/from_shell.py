from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls as sfpc
from pygments.styles import get_all_styles, get_style_by_name
from pygments.util import ClassNotFound

from piston.colorschemes import scheme_dict, schemes
from piston.utils import helpers, services
from piston.utils.compilers import languages_
from piston.utils.constants import CONSOLE, PistonQuery, Shell
from piston.utils.lexers import lexers_dict
from piston.utils.prompt_continuation import prompt_continuation


class FromShell:
    """Run code from a shell environment."""

    def __init__(self):
        self.themes = list(get_all_styles()) + schemes
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

    def set_style(self, theme: str) -> None:
        """Set the theme for prompt_toolkit."""
        if theme in self.themes:
            try:
                self.style = sfpc(get_style_by_name(theme))
            except ClassNotFound:
                self.style = scheme_dict[theme]()
        else:
            CONSOLE.print(
                f"[red]Theme {theme} is not a valid theme, using piston-cli default"
            )
            self.style = sfpc(get_style_by_name("solarized-dark"))

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
        self.set_style(theme)

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
