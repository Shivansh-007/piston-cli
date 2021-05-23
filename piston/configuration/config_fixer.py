from piston.configuration.validators.prompt_validator import (
    PromptContinuationValidator,
    PromptStartValidator,
)
from piston.configuration.validators.theme_validator import ThemeValidator


def fix_config(config: dict) -> None:
    """Validates and fixes a configuration dictionary temporarily."""
    config["theme"] = ThemeValidator(config["theme"]).fix_theme()

    config["prompt_start"] = PromptStartValidator(config["prompt_start"]).fix_prompt()

    config["prompt_continuation"] = PromptContinuationValidator(
        config["prompt_continuation"]
    ).fix_prompt()
