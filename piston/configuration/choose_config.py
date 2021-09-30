import random
from typing import Any

import rich


def choose_config(console: rich.console.Console, config: Any) -> Any:
    """Chooses a random value from a list of config options or returns the config if it is not in a list."""
    if isinstance(config, list):
        choice = random.choice(config)
        console.print(f"[blue]Chose {choice}.[/blue]")
        return choice
    return config
