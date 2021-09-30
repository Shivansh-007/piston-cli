from dataclasses import dataclass
from pathlib import Path
from typing import List

from appdirs import user_cache_dir, user_config_dir
from pygments.styles import get_all_styles

SPINNERS = [
    "point",
    "dots",
    "dots12",
    "dots9",
    "dots2",
    "simpleDotsScrolling",
    "bouncingBall",
]

themes = list(set(get_all_styles()))

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

THEME_PREVIEW = '''
def print_square(num: int = 20) -> str:
    """Output the square of a number."""
    result = num ** 2
    return f"The square of {num:.2} is {result:.2}."
'''

CACHE_LOCATION = Path(user_cache_dir("piston-cli"))
REQUEST_CACHE_LOCATION = Path(CACHE_LOCATION, ".piston_cache")
REQUEST_CACHE_DURATION = 60 * 60 * 24


class Configuration:
    configuration_path = (
        Path(user_config_dir("piston-cli"), "config.yaml"),
        Path(user_config_dir("piston-cli"), "config.yml"),
    )

    default_configuration = {
        "theme": "solarized-dark",
        "box_style": "HORIZONTALS",
        "prompt_start": ">>>",
        "prompt_continuation": "...",
    }


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
