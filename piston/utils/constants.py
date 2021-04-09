import os
from dataclasses import dataclass
from typing import List

from pygments.styles import get_all_styles
from piston.colorschemes import schemes
from piston.utils.compilers import languages_
from rich.console import Console

CONSOLE = Console()

SPINNERS = [
    "point",
    "dots",
    "dots12",
    "dots9",
    "dots2",
    "simpleDotsScrolling",
    "bouncingBall",
]

themes = list(get_all_styles()) + schemes
THEMES = [list(themes[style: style + 2]) for style in range(0, len(themes), 2)]

LANG_TABLE = zip(iter(languages_), iter(languages_))


class Configuration:
    configuration_paths = {
        "Windows": (
            os.path.expandvars("%APPDATA%/piston-cli/config.yaml"),
            os.path.expandvars("%APPDATA%/piston-cli/config.yml"),
        ),
        "Darwin": (
            os.path.expandvars("$HOME/.config/piston-cli/config.yaml"),
            os.path.expandvars("$HOME/.config/piston-cli/config.yml"),
        ),
        "Linux": (
            os.path.expandvars("$HOME/.config/piston-cli/config.yaml"),
            os.path.expandvars("$HOME/.config/piston-cli/config.yml"),
        ),
    }

    default_configuration = {"theme": "solarized-dark"}


class Shell:
    prompt_start = ">>> "
    prompt_continuation = "... "


@dataclass
class PistonQuery:
    """Represents the payload sent to the Piston API."""

    language: str
    code: str
    args: List[str]
    stdin: str
