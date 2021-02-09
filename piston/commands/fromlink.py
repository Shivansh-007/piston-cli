import json
import random
import urllib
from typing import List, Optional, Union

import requests
from piston.colorschemes import schemes
from piston.utilities.compilers import languages_
from piston.utilities.constants import init_lexers, spinners
from piston.utilities.utils import Utils
from pygments.styles import get_all_styles
from rich.console import Console


class FromLink:
    """TODO: Write a Docstring here."""

    def __init__(self) -> None:
        init_lexers()
        self.languages = languages_

        self.console = Console()
        self.output_json = dict()
        self.spinners = spinners
        self.themes = list(get_all_styles()) + schemes

    def get_lang(self) -> str:
        """Prompt the user for the programming language, close program if language not supported."""
        language = self.console.input("[green]Enter language:[/green] ").lower()

        if language not in self.languages:
            self.console.print("Language is not supported!", style="bold red")
            Utils.close()
        return language

    def get_args(self) -> List[str]:
        """Prompt the user for the command line arguments."""
        args = self.console.input(
            "[green]Enter your args separated by comma:[/green] "
        ).lower()
        return [x for x in args.strip().split(",") if x]

    def get_stdin(self) -> str:
        """Prompt the user for the standard input."""
        stdin = self.console.input(
            "[green]Enter your stdin arguments:[/green] "
        ).lower()
        return stdin

    def get_code(self) -> Union[bool, str]:
        """Prompt the user for the pastebin link."""
        link = self.console.input("[green]Enter the link:[/green] ").lower()

        base_url = urllib.parse.quote_plus(
            link.split(" ")[-1][5:].strip("/"), safe=";/?:@&=$,><-[]"
        )

        domain = base_url.split("/")[2]
        if domain == "paste.pythondiscord.com":
            if "/raw/" in base_url:
                url = base_url
            token = base_url.split("/")[-1]
            if "." in token:
                token = token[: token.rfind(".")]  # removes extension
            url = f"https://paste.pythondiscord.com/raw/{token}"
        else:
            self.console.print(
                "Can only accept links from paste.pythondiscord.com.", style="red"
            )
            return False

        response = requests.get(url)
        if response.status_code == 404:
            self.console.print("Nothing found. Check your link", style="red")
            return False
        elif response.status_code != 200:
            self.console.print(
                f"An error occurred (status code: {response.status_code}). ",
                style="red",
            )
            return False
        return response.text

    def askinp(self) -> Optional[str]:
        """
        Make a multiline prompt for code input and send the code to the api.

        The compiled output from the api is returned.
        """
        language = self.get_lang()
        args = self.get_args()
        stdin = self.get_stdin()
        code = self.get_code()

        if not code:
            return

        self.output_json = {
            "language": language,
            "source": code,
            "args": args,
            "stdin": stdin,
        }

        with self.console.status(
            "Compiling", spinner=random.choice(self.spinners)
        ) as _:
            data = requests.post(
                "https://emkc.org/api/v1/piston/execute",
                data=json.dumps(self.output_json),
            ).json()

        if len(data["output"]) == 0:
            return "Your code ran without output."
        else:
            result = [
                f"{i:02d} | {line}"
                for i, line in enumerate(data["output"].split("\n"), 1)
            ]
            return "\n".join(result)


FromLink = FromLink()
