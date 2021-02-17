#!/usr/bin/env python3

import os
import sys

from piston.commands import commands_dict
from piston.utilities.constants import languages_table, themes
from piston.utilities.maketable import MakeTable
from piston.utilities.utils import Utils
from rich.console import Console


def main() -> None:
    """TODO: Write a Docstring here."""
    console = Console()

    args = commands_dict["base"]()

    output = None

    if args.list:
        console.print(MakeTable.mktbl(languages_table))
        Utils.close()

    if args.themelist:
        console.print(MakeTable.mktbl(themes))
        Utils.close()

    elif args.file:
        output, language = commands_dict["from_file"](args.file)

    elif args.link:
        output, language = commands_dict["from_link"]()

    elif args.shell:
        try:
            commands_dict["from_shell"](args.shell, args.theme)
        except KeyboardInterrupt:
            pass

    else:
        output, language = commands_dict["from_input"](args.theme)

    if output:
        width = os.get_terminal_size().columns - 5
        console.print(f"\nHere is your {language} output:", style="green")
        console.print(Utils.print_msg_box(output, width=width))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Error:\n{e}")
