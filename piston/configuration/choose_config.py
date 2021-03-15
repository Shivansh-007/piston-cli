from typing import Any
import random

from piston.utilities.constants import console


def choose_config(config: Any) -> Any:
	if type(config) is list:
		choice = random.choice(config)
		console.print(f"[blue]Chose {choice}.[/blue]")
		return choice
	return config