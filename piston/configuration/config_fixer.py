from piston.configuration.validators.message_box_validator import MessageBoxValidator
from piston.configuration.validators.theme_validator import ThemeValidator


def fix_config(config: dict) -> None:
    """Validates and fixes a configuration dictionary temporarily."""
    config["theme"] = ThemeValidator(config["theme"]).fix_theme()
    config["message_box"] = MessageBoxValidator(config["message_box"]).fix_box_style()
