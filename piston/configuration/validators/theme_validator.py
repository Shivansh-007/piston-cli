from typing import Union

from piston.configuration.choose_config import choose_config
from piston.configuration.validators.validator_base import Validator
from piston.utilities.constants import Configuration, themes


class ThemeValidator(Validator):

    def __init__(self, themes: Union[str, list]) -> None:
        self.themes = themes
        self.default_theme = Configuration.default_configuration["theme"]
        super().__init__(self.themes, self.default_theme, "theme")
    
    @staticmethod
    def check_theme_exists(theme: str) -> bool:
        if theme not in themes:
            console.print(
                f"[red]Theme invalid, \"{theme}\" not recognized. Using default theme.[/red]"
            )
            return False
        return True

    def validate_theme(self) -> bool:
        """Validates a theme string."""

        if not self.validate_type():
            return False

        if type(self.themes) is str and not ThemeValidator.check_theme_exists(self.themes):  # Check the singular theme exists.
            return False

        if type(self.themes) is list:  # Check each theme exists.
            for theme in self.themes:
                if not ThemeValidator.check_theme_exists(theme):
                    return False

        return True

    def fix_theme(self) -> str:
        if self.validate_theme():
            return choose_config(self.themes)
        return self.default_theme
            
