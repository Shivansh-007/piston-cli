from typing import Any

from piston.utils.constants import CONSOLE


class Validator:
    """Base class for all other configuration validators that provides some basic checks."""

    def __init__(self, config: Any, config_default: Any, name: str) -> None:
        self.config = config
        self.config_default = config_default
        self.current_type = type(config)
        self.target_type = type(config_default)

        self.name = name

    def validate_type(self) -> bool:
        """Validates the type of a given configuration."""
        if self.current_type is not self.target_type and self.current_type is not list:
            CONSOLE.print(
                f'[red]Configuration "{self.config.__name__}" invalid, use type {self.target_type.__name__}, '
                f"not {self.current_type.__name__}. Using default setting.[/red]"
            )
            return False

        if self.current_type is list:
            for item in self.config:
                if not isinstance(item, self.target_type):
                    CONSOLE.print(
                        f'[red]A possible "{item}" in the list of "{self.name}" configurations '
                        f"specified has an invalid type, use type {self.target_type.__name__}. "
                        f"not {type(item).__name__}. Using default setting.[/red]"
                    )
                    return False

            CONSOLE.print(
                f'[blue]A list of possible configurations was found for the "{self.name}" option. '
                "Choosing a random one."
            )

        return True
