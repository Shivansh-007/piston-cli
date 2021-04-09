import os
import sys
from typing import List

from piston.utils.compilers import languages_
from piston.utils.constants import CONSOLE


def close() -> None:
    """Exit the program."""
    try:
        sys.exit(1)
    except SystemExit:
        os._exit(1)


def print_msg_box(
        msg: str,
        indent: int = 1,
        width: int = 0,
        title: str = ""
) -> str:
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


def get_lang():
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
    args = CONSOLE.input("[green]Enter your args separated by comma:[/green] ")
    return [x for x in args.strip().split(",") if x]


def get_stdin() -> str:
    """Prompt the user for the standard input."""
    stdin = CONSOLE.input(
        "[green]Enter your stdin arguments by comma:[/green] "
    )
    return "\n".join([x for x in stdin.strip().split(",") if x])

