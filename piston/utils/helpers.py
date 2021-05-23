import os
import shlex
import sys

from prompt_toolkit.styles import Style
from prompt_toolkit.styles.pygments import style_from_pygments_cls as sfpc
from pygments.styles import get_style_by_name
from pygments.util import ClassNotFound
from rich import box
from rich.table import Table

from piston.colorschemes import scheme_dict
from piston.utils.compilers import languages_
from piston.utils.constants import CONSOLE, themes


def parse_string(string: str) -> list[str]:
    """Parse string like python string parsing with the help of backslash."""
    parsed_string = shlex.shlex(string, posix=True)
    parsed_string.escapedquotes = "\"'"
    return list(parsed_string)


def close() -> None:
    """Exit the program."""
    try:
        sys.exit(1)
    except SystemExit:
        os._exit(1)


def print_msg_box(msg: str, style: str = "HORIZONTALS") -> Table:
    """Print message-box with optional style, passed from user's configuration."""
    style = getattr(box, style)

    table = Table(title="", show_header=False, box=style, title_justify="left")
    table.add_column("Line No.", style="magenta")
    table.add_column("Output")

    # Hotfix for each character being on its own line when no output.
    if isinstance(msg, str):
        msg = msg.split("\n")

    for x, line in enumerate(msg, 1):
        table.add_row(str(x), line)

    return table


def get_lang() -> str:
    """
    Prompt the user for the programming language.

    If language is not supported then exit the CLI.
    """
    language = CONSOLE.input("[green]Enter language:[/green] ").lower()

    if language not in languages_:
        CONSOLE.print("[bold red]Language is not supported![/bold red]")
        close()
    return language


def get_args() -> list[str]:
    """Prompt the user for the command line arguments."""
    args = CONSOLE.input("[green]Enter your args separated:[/green] ")
    return parse_string(args)


def get_stdin() -> str:
    """Prompt the user for the standard input."""
    stdin = CONSOLE.input("[green]Enter your stdin arguments:[/green] ")
    return "\n".join(parse_string(stdin))


def set_style(theme: str) -> Style:
    """Set the theme for prompt_toolkit."""
    if theme in themes:
        try:
            style = sfpc(get_style_by_name(theme))
        except ClassNotFound:
            style = sfpc(scheme_dict[theme])
    else:
        CONSOLE.print(
            f"[red]Theme {theme} is not a valid theme, using piston-cli default"
        )
        style = sfpc(get_style_by_name("solarized-dark"))

    return style
