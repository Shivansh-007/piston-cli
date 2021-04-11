#!/usr/bin/env python3

import os
import sys

from piston.commands import commands_dict
from piston.configuration.config_loader import ConfigLoader
from piston.utils import helpers
from piston.utils.constants import LANG_TABLE, THEMES
from piston.utils.maketable import MakeTable
from rich.console import Console


def main() -> None:
    """TODO: Write a Docstring here."""
    console = Console()

    args = commands_dict["base"]()

    output = None

    config_loader = ConfigLoader(args.config)
    config = config_loader.load_config()

    if args.list:
        console.print(MakeTable.mktbl(LANG_TABLE))
        helpers.close()

    if args.themelist:
        console.print(MakeTable.mktbl(THEMES))
        helpers.close()

    elif args.file:
        output, language = commands_dict["from_file"](args.file)

    elif args.link:
        output, language = commands_dict["from_link"]()

    elif args.shell:
        try:
            commands_dict["from_shell"](args.shell, args.theme or config["theme"])
        except KeyboardInterrupt:
            pass

    else:
        output, language = commands_dict["from_input"](args.theme or config["theme"])

    if output:
        width = os.get_terminal_size().columns - 5
        console.print(f"\n[green]Here is your {language} output:[/green]")
        console.print(helpers.print_msg_box(output, width=width))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Error:\n{e}")
