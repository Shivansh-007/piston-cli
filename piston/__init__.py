#!/usr/bin/env python3

import sys

from more_itertools import grouper

from piston import version
from piston.commands import commands_dict
from piston.configuration.config_loader import ConfigLoader
from piston.utils import helpers
from piston.utils.compilers import languages_
from piston.utils.constants import BOX_STYLES, CONSOLE
from piston.utils.lexers import init_lexers
from piston.utils.maketable import make_table


def main() -> None:
    """Implement the main piston-cli process."""
    args = commands_dict["base"]()

    if args.version:
        print(version.__version__, flush=True)
        helpers.close()

    if args.list:
        list_commands = {
            "themes": commands_dict["theme_list"],
            "languages": ("Languages", grouper(languages_, 2)),
            "boxes": ("Box Styles", grouper(BOX_STYLES, 2)),
        }
        try:
            # If the value is an tuple i.e. it is formatted for a box.
            if isinstance(list_commands[args.list], tuple):
                table = make_table(*list_commands[args.list])
                CONSOLE.print(table)
            else:
                # Else it is just a callable and we can call it.
                list_commands[args.list]()
        except KeyError:
            CONSOLE.print(
                f"[red] Invalid option provided - Valid "
                f"options include:[/red] [cyan]{', '.join(list_commands.keys())}[/cyan]"
            )

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

    if args.file:
        output, language = commands_dict["from_file"](args.file)

    elif args.pastebin:
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
