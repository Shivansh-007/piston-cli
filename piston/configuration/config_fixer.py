from piston.configuration.validators.theme_validator import ThemeValidator
from piston.utilities.constants import Configuration


def fix_config(config: dict) -> None:
    """Validates and fixes a configuration dictionary temporarily."""
    config["theme"] = ThemeValidator(config["theme"]).fix_theme()
