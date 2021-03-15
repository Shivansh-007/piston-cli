import random
from typing import Any

from piston.utilities.constants import console


def choose_config(config: Any) -> Any:
    """Chooses a random value from a list of config options or returns the config if it is not in a list."""
    if type(config) is list:
        choice = random.choice(config)
        console.print(f"[blue]Chose {choice}.[/blue]")
        return choice
    return config
