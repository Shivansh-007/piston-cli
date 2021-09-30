import urllib
from typing import Optional, Union

import requests
from pygments.styles import get_all_styles

from piston.utils import helpers, services
from piston.utils.constants import CONSOLE, PistonQuery


THEMES = list(get_all_styles())


def get_code(link: str) -> Union[bool, str]:
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
        CONSOLE.print("[red]Can only accept links from paste.pythondiscord.com.[/red]")
        return False

    response = requests.get(url)
    if response.status_code == 404:
        CONSOLE.print("[red]Nothing found. Check your link[/red]")
        return False
    elif response.status_code != 200:
        CONSOLE.print(f"[red]An error occurred (status code: {response.status_code}).[/red]")
        return False
    return response.text


def run_link(link: str, language: str) -> Optional[Union[list, str]]:
    """
    Make a multiline prompt for code input and send the code to the api.

    The compiled output from the api is returned.
    """
    args = helpers.get_args()
    stdin = helpers.get_stdin()
    code = get_code(link)

    if not code:
        return

    payload = PistonQuery(language=language, args=args, stdin=stdin, code=code)
    data = services.query_piston(CONSOLE, payload)

    if len(data["output"]) == 0:
        return "Your code ran without output."

    return data["output"].split("\n")

