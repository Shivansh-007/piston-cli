import rich

from piston.configuration.validators.box_validator import BoxStyleValidator
from piston.configuration.validators.prompt_validator import PromptContinuationValidator, PromptStartValidator
from piston.configuration.validators.theme_validator import ThemeValidator


def fix_config(console: rich.console.Console, config: dict) -> None:
    """Validates and fixes a configuration dictionary temporarily."""
    config["theme"] = ThemeValidator(console, config["theme"]).fix_theme()
    config["box_style"] = BoxStyleValidator(console, config["box_style"]).fix_box_style()

    config["prompt_start"] = PromptStartValidator(console, config["prompt_start"]).fix_prompt()
    config["prompt_continuation"] = PromptContinuationValidator(
        console, config["prompt_continuation"]
    ).fix_prompt()
