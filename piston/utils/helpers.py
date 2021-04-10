import os
import shlex
import sys
from typing import List

from piston.utils.compilers import languages_
from piston.utils.constants import CONSOLE


def parse_string(string: str) -> List[str]:
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


def print_msg_box(msg: str, indent: int = 1, width: int = 0, title: str = "") -> str:
    """Print message-box with optional title."""
    lines = msg.split("\n")
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'┏{"━" * (width + indent * 2)}┓\n'
    if title:
        box += f"┃{space}{title:<{width}}{space}┃\n"
        box += f'┃{space}{"-" * len(title):<{width}}{space}┃\n'
    box += "".join([f"┃{space}{line:<{width}}{space}┃\n" for line in lines])
    box += f'┗{"━" * (width + indent * 2)}┛'
    return box


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


def get_args() -> List[str]:
    """Prompt the user for the command line arguments."""
    args = CONSOLE.input("[green]Enter your args separated:[/green] ")
    return parse_string(args)


def get_stdin() -> str:
    """Prompt the user for the standard input."""
    stdin = CONSOLE.input("[green]Enter your stdin arguments:[/green] ")
    return "\n".join(parse_string(stdin))
