from typing import Union

from piston.configuration.choose_config import choose_config
from piston.configuration.validators.validator_base import Validator
from piston.utils.constants import CONSOLE, Configuration, themes


class ThemeValidator(Validator):
    """Validates a string or list of themes by checking multiple criteria."""

    def __init__(self, themes: Union[str, list]) -> None:
        self.themes = themes
        self.default_theme = Configuration.default_configuration["theme"]
        super().__init__(self.themes, self.default_theme, "theme")

    @staticmethod
    def check_theme_exists(theme: str) -> bool:
        """Ensures that a given theme exists."""
        if theme not in themes:
            CONSOLE.print(
                f'[red]Theme invalid, "{theme}" not recognized. Using default theme.[/red]'
            )
            return False
        return True

    def validate_theme(self) -> bool:
        """Validates a theme string."""
        if not self.validate_type():
            return False

        if isinstance(self.themes, str) and not ThemeValidator.check_theme_exists(
            self.themes
        ):  # Check the singular theme exists.
            return False

        if isinstance(self.themes, list):  # Check each theme exists.
            for theme in self.themes:
                if not ThemeValidator.check_theme_exists(theme):
                    return False

        return True

    def fix_theme(self) -> str:
        """Finds and corrects any errors in a given theme or list of themes, then returns a fixed version."""
        if self.validate_theme():
            return choose_config(self.themes)
        return self.default_theme
