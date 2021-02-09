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

    if args.list:
        console.print(MakeTable.mktbl(languages_table))
        Utils.close()

    if args.themelist:
        console.print(MakeTable.mktbl(themes))
        Utils.close()

    elif args.file:
        output = commands_dict["fromfile"](args.file)

    elif args.link:
        output = commands_dict["fromlink"]()

    else:
        output = commands_dict["frominput"](args.theme)

    width = os.get_terminal_size().columns - 5

    if output:
        console.print("\nHere is your output:", style="green")
        console.print(Utils.print_msg_box(output, width=width))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Error:\n{e}")
