import json
import random
from typing import List, Tuple

import requests
from piston.utilities.constants import spinners
from piston.utilities.lang_extensions import lang_extensions
from piston.utilities.utils import Utils
from rich.console import Console


class FromFile:
    """TODO: Write a Docstring here."""

    def __init__(self) -> None:
        self.console = Console()
        self.output_json = dict()
        self.spinners = spinners

        self.extensions = lang_extensions

    def get_args(self) -> List[str]:
        """Prompt the user for the programming language, close program if language not supported."""
        args = self.console.input("[green]Enter your args separated by comma:[/green] ")
        return [x for x in args.strip().split(",") if x]

    def get_stdin(self) -> str:
        """Prompt the user for the programming language, close program if language not supported."""
        stdin = self.console.input(
            "[green]Enter your stdin arguments by comma:[/green] "
        )
        return "\n".join([x for x in stdin.strip().split(",") if x])

    def runfile(self, file: str) -> Tuple[str, str]:
        """Send code form file to the api and return the response."""
        args = self.get_args()
        stdin = self.get_stdin()

        try:
            code = open(file)
            code = code.read()

            if not any(file.endswith("." + ext) for ext in self.extensions):
                self.console.print(
                    "File Extension language is not supported!", style="bold red"
                )
                Utils.close()

        except FileNotFoundError:
            self.console.print("Path is invalid; File not found", style="bold red")
            Utils.close()

        language = self.extensions[file[file.rfind(".") + 1 :]]
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
            return "Your code ran without output.", language
        else:
            result = [
                f"{i:02d} | {line}"
                for i, line in enumerate(data["output"].split("\n"), 1)
            ]
            return "\n".join(result), language


FromFile = FromFile()
