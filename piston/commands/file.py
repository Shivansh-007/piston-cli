from typing import Union

import click

from piston.utils import helpers, services
from piston.utils.constants import PistonQuery
from piston.utils.lang_extensions import lang_extensions


def run_file(ctx: click.Context, file: str, args: list[str] = None) -> Union[list, str]:
    """Send code form file to the api and return the response."""
    console = ctx.obj["console"]
    if not args:
        args = helpers.get_args(console)
    stdin = helpers.get_stdin(console)

    try:
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()

        if not any(file.endswith("." + ext) for ext in lang_extensions):
            console.print("File Extension language is not supported!", style="bold red")
            ctx.exit()

    except FileNotFoundError:
        console.print("Path is invalid; File not found", style="bold red")
        ctx.exit()

    language = lang_extensions[file[file.rfind(".") + 1 :]]

    payload = PistonQuery(
        language=language,
        code=code,
        args=args,
        stdin=stdin,
    )

    data = services.query_piston(ctx, console, payload)

    if len(data["output"]) == 0:
        return "Your code ran without output."

    return data["output"].split("\n")
