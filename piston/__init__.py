#!/usr/bin/env python3

import sys

from piston.commands import commands_dict
from piston.configuration.config_loader import ConfigLoader
from piston.utils import helpers
from piston.utils.constants import CONSOLE, LANG_TABLE, THEMES
from piston.utils.lexers import init_lexers
from piston.utils.maketable import MakeTable


def main() -> None:
    """TODO: Write a Docstring here."""
    init_lexers()

    args = commands_dict["base"]()
    output = None

    config_loader = ConfigLoader(args.config)
    config = config_loader.load_config()

    if args.theme:
        CONSOLE.print(
            f"[indian_red]- Theme flag specified, overwriting theme loaded from "
            f"config: {args.theme}[/indian_red]"
        )

    if args.list:
        CONSOLE.print(MakeTable.mktbl(LANG_TABLE))
        helpers.close()

    if args.themelist:
        commands_dict["theme_list"]()
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
        CONSOLE.print("")  # Blank line
        CONSOLE.print(
            helpers.print_msg_box(
                output,
                title=f"Here is your {language} output:",
                style=config["message_box"],
            )
        )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Error:\n{e}")
