from piston.configuration.validators.box_validator import BoxStyleValidator
from piston.configuration.validators.theme_validator import ThemeValidator


def fix_config(config: dict) -> None:
    """Validates and fixes a configuration dictionary temporarily."""
    config["theme"] = ThemeValidator(config["theme"]).fix_theme()
    config["box_style"] = BoxStyleValidator(config["box_style"]).fix_box_style()
