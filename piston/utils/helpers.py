import random
import shlex
import sys
from signal import SIGINT

import rich
from prompt_toolkit.styles import Style
from prompt_toolkit.styles.pygments import style_from_pygments_cls as sfpc
from pygments.styles import get_style_by_name
from pygments.util import ClassNotFound
from rich import box
from rich.table import Table

from piston.utils.constants import themes


def parse_string(string: str) -> list[str]:
    """Parse string like python string parsing with the help of backslash."""
    parsed_string = shlex.shlex(string, posix=True)
    parsed_string.escapedquotes = "\"'"
    return list(parsed_string)


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


def get_args(console: rich.console.Console) -> list[str]:
    """Prompt the user for the command line arguments."""
    args = console.input("[green]Enter your args separated:[/green] ")
    return parse_string(args)


def get_stdin(console: rich.console.Console) -> str:
    """Prompt the user for the standard input."""
    stdin = console.input("[green]Enter your stdin arguments:[/green] ")
    return "\n".join(parse_string(stdin))


def set_style(console: rich.console.Console, theme: str) -> Style:
    """Set the theme for prompt_toolkit."""
    if theme in themes:
        try:
            style = sfpc(get_style_by_name(theme))
        except ClassNotFound:
            console.print(f"[red]Theme {theme} is not a valid theme, using piston-cli default")
            style = sfpc(get_style_by_name("solarized-dark"))
    else:
        console.print(f"[red]Theme {theme} is not a valid theme, using piston-cli default")
        style = sfpc(get_style_by_name("solarized-dark"))

    return style


def signal_handler(console: rich.console.Console, sig: int, frame: any) -> None:
    """Handles Signals (E.g. SIGINT)."""
    messages = ["Goodbye!", "See you next time!", "Bye bye!"]
    if sig == SIGINT:  # If SIGINT - Close application
        console.print(f"\n\n{random.choice(messages)}\n")
        sys.exit(0)
    else:  # If an unhandled signal is received - Shut down with relevant information.
        console.print(f"\n\n[red]Unexpected signal ({sig}) received - {random.choice(messages)}\n[/red]")
        sys.exit(sig)
