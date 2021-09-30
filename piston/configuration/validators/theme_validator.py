from typing import Union

import rich

from piston.configuration.choose_config import choose_config
from piston.configuration.validators.validator_base import Validator
from piston.utils.constants import Configuration, themes


class ThemeValidator(Validator):
    """Validates a string or list of themes by checking multiple criteria."""

    def __init__(self, console: rich.console.Console, themes: Union[str, list]) -> None:
        self.console = console
        self.themes = themes
        self.default_theme = Configuration.default_configuration["theme"]
        super().__init__(self.console, self.themes, self.default_theme, "theme")

    def check_theme_exists(self, theme: str) -> bool:
        """Ensures that a given theme exists."""
        if theme not in themes:
            self.console.print(f'[red]Theme invalid, "{theme}" not recognized. Using default theme.[/red]')
            return False
        return True

    def validate_theme(self) -> bool:
        """Validates a theme string."""
        if not self.validate_type():
            return False

        if isinstance(self.themes, str) and not self.check_theme_exists(self.themes):
            # Check the singular theme exists.
            return False

        if isinstance(self.themes, list):  # Check each theme exists.
            for theme in self.themes:
                if not self.check_theme_exists(theme):
                    return False

        return True

    def fix_theme(self) -> str:
        """Finds and corrects any errors in a given theme or list of themes, then returns a fixed version."""
        if self.validate_theme():
            return choose_config(self.console, self.themes)
        return self.default_theme
