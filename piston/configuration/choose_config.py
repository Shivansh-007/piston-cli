import random
from typing import Any

from piston.utils.constants import CONSOLE


def choose_config(config: Any) -> Any:
    """Chooses a random value from a list of config options or returns the config if it is not in a list."""
    if isinstance(config, list):
        choice = random.choice(config)
        CONSOLE.print(f"[blue]Chose {choice}.[/blue]")
        return choice
    return config
