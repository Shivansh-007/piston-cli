#!/usr/bin/env python3

import sys

from piston import __version__
from piston.commands import commands_dict
from piston.configuration.config_loader import ConfigLoader
from piston.utils import helpers
from piston.utils.constants import CONSOLE, LANG_TABLE, THEMES
from piston.utils.lexers import init_lexers
from piston.utils.maketable import MakeTable


def main() -> None:
    """TODO: Write a Docstring here."""
    args = commands_dict["base"]()

    if args.version:
        print(__version__.__version__, flush=True)
        helpers.close()

    if args.list:
        CONSOLE.print(MakeTable.mktbl(LANG_TABLE))
        helpers.close()

    if args.themelist:
        commands_dict["theme_list"]()
        helpers.close()

    config_loader = ConfigLoader(args.config)
    config = config_loader.load_config()
    output = None
    init_lexers()

    if args.theme:
        CONSOLE.print(
            f"[indian_red]- Theme flag specified, overwriting theme loaded from "
            f"config: {args.theme}[/indian_red]"
        )

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
        CONSOLE.print(f"\nHere is your {language} output:")
        CONSOLE.print(
            helpers.print_msg_box(
                output,
                style=config["box_style"],
            )
        )
        helpers.close()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Error:\n{e}")
