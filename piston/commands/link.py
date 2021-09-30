import urllib
from typing import Optional, Union

import click
import requests
import rich
from pygments.styles import get_all_styles

from piston.utils import helpers, services
from piston.utils.constants import PistonQuery

THEMES = list(get_all_styles())


def get_code(console: rich.console.Console, link: str) -> Union[bool, str]:
    """Prompt the user for the pastebin link."""
    base_url = urllib.parse.quote_plus(link.split(" ")[-1][5:].strip("/"), safe=";/?:@&=$,><-[]")

    domain = base_url.split("/")[2]
    if domain == "paste.pythondiscord.com":
        if "/raw/" in base_url:
            url = base_url
        token = base_url.split("/")[-1]
        if "." in token:
            token = token[: token.rfind(".")]  # removes extension
        url = f"https://paste.pythondiscord.com/raw/{token}"
    else:
        console.print("[red]Can only accept links from paste.pythondiscord.com.[/red]")
        return False

    response = requests.get(url)
    if response.status_code == 404:
        console.print("[red]Nothing found. Check your link[/red]")
        return False
    elif response.status_code != 200:
        console.print(f"[red]An error occurred (status code: {response.status_code}).[/red]")
        return False
    return response.text


def run_link(ctx: click.Context, link: str, language: str) -> Optional[Union[list, str]]:
    """
    Make a multiline prompt for code input and send the code to the api.

    The compiled output from the api is returned.
    """
    console = ctx.obj["console"]
    args = helpers.get_args(console)
    stdin = helpers.get_stdin(console)
    code = get_code(console, link)

    if not code:
        return

    payload = PistonQuery(language=language, args=args, stdin=stdin, code=code)
    data = services.query_piston(ctx, console, payload)

    if len(data["output"]) == 0:
        return "Your code ran without output."

    return data["output"].split("\n")
