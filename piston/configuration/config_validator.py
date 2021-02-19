from piston.configuration.validators import theme_validator
from piston.utilities.constants import Configuration


def validate_config(config: dict) -> None:
    """Validates and fixes a configuration dictionary temporarily."""
    if not theme_validator.validate_theme(config["theme"]):
        config["theme"] = Configuration.default_configuration["theme"]
