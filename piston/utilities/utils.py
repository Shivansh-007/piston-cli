import os
import sys


class Utils:
    """TODO: Write a Docstring here."""

    def close(self) -> None:
        """Exit the program."""
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)

    def print_msg_box(
        self, msg: str, indent: int = 1, width: int = 0, title: str = ""
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


Utils = Utils()
