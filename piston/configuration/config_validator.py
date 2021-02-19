from piston.configuration.validators import theme_validator
from piston.utilities.constants import Configuration, console


def validate_config(config: dict):
    if not theme_validator.validate_theme(config["theme"]):
        config["theme"] = Configuration.default_configuration["theme"]
