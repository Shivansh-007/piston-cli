import os
from dataclasses import dataclass
from typing import List

from pygments.styles import get_all_styles
from rich.console import Console

from piston.colorschemes import schemes

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

BOX_STYLES = [
    "ASCII",
    "ASCII2",
    "ASCII_DOUBLE_HEAD",
    "SQUARE",
    "SQUARE_DOUBLE_HEAD",
    "MINIMAL",
    "MINIMAL_HEAVY_HEAD",
    "MINIMAL_DOUBLE_HEAD",
    "SIMPLE",
    "SIMPLE_HEAD",
    "SIMPLE_HEAVY",
    "HORIZONTALS",
    "ROUNDED",
    "HEAVY",
    "HEAVY_EDGE",
    "HEAVY_HEAD",
    "DOUBLE",
    "DOUBLE_EDGE",
]


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

    default_configuration = {"theme": "solarized-dark", "box_style": "HORIZONTALS"}


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
