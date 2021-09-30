from typing import Union

import click
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.shortcuts import prompt

from piston.utils import helpers, services
from piston.utils.constants import PistonQuery
from piston.utils.lexers import lexers_dict


def user_input(ctx: click.Context, theme: str, language: str) -> Union[tuple, str]:
    """
    Make a multiline prompt for code input and send the code to the api.

    The compiled output from the api is returned.
    """
    console = ctx.obj["console"]
    args = helpers.get_args(console)
    stdin = helpers.get_stdin(console)

    console.print("[green]Enter your code, (press esc + enter to run)[/green]")
    style = helpers.set_style(console, theme)

    console.print()
    code = prompt(
        "",
        lexer=PygmentsLexer(lexers_dict[language]),
        include_default_pygments_style=False,
        style=style,
        multiline=True,
    )
    payload = PistonQuery(language=language, args=args, stdin=stdin, code=code)

    data = services.query_piston(ctx, console, payload)

    if len(data["output"]) == 0:
        return "Your code ran without output.", language

    return data["output"].split("\n"), language
