from typing import Union

from piston.utils import helpers, services
from piston.utils.constants import CONSOLE, PistonQuery
from piston.utils.lang_extensions import lang_extensions


class FromFile:
    """Run code from file."""

    def __init__(self) -> None:
        self.extensions = lang_extensions

    def run_file(self, file: str) -> Union[tuple, str]:
        """Send code form file to the api and return the response."""
        args = helpers.get_args()
        stdin = helpers.get_stdin()

        try:
            with open(file, "r", encoding="utf-8") as f:
                code = f.read()

            if not any(file.endswith("." + ext) for ext in self.extensions):
                CONSOLE.print(
                    "File Extension language is not supported!", style="bold red"
                )
                helpers.close()

        except FileNotFoundError:
            CONSOLE.print("Path is invalid; File not found", style="bold red")
            helpers.close()

        language = self.extensions[file[file.rfind(".") + 1 :]]

        payload = PistonQuery(
            language=language,
            code=code,
            args=args,
            stdin=stdin,
        )

        data = services.query_piston(CONSOLE, payload)

        if len(data["output"]) == 0:
            return "Your code ran without output.", language

        return data["output"].split("\n"), language


FromFile = FromFile()
