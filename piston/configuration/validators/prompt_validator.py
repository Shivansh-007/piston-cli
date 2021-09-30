import rich

from piston.configuration.choose_config import choose_config
from piston.configuration.validators.validator_base import Validator
from piston.utils.constants import Configuration


class PromptStartValidator(Validator):
    """Validates the prompt_start config variable."""

    def __init__(self, console: rich.console.Console, prompt: str) -> None:
        self.console = console
        self.prompt = prompt
        self.default_prompt = Configuration.default_configuration["prompt_start"]
        super().__init__(self.console, self.prompt, self.default_prompt, "prompt_start")

    def validate_prompt(self) -> bool:
        """Validates prompt start."""
        if not self.validate_type():
            return False

        # Make sure there are no new lines in the prompt
        if "\n" in self.prompt or "\r" in self.prompt:
            return False

        return True

    def fix_prompt(self) -> str:
        """Fixes the prompt_start configuration variables."""
        if self.validate_prompt():
            return choose_config(self.console, self.prompt)
        self.console.print(
            f"[red]Prompt start invalid. {repr(self.prompt)} contains a new"
            "line character. Using default prompt start instead.[/red]"
        )
        return self.default_prompt


class PromptContinuationValidator(Validator):
    """Validates the prompt_continuation config variable."""

    def __init__(self, console: rich.console.Console, prompt: str) -> None:
        self.console = console
        self.prompt = prompt
        self.default_prompt = Configuration.default_configuration["prompt_continuation"]
        super().__init__(self.console, self.prompt, self.default_prompt, "prompt_continuation")

    def validate_prompt(self) -> bool:
        """Validates prompt continuation."""
        if not self.validate_type():
            return False

        # Make sure there are no new lines in the prompt
        if "\n" in self.prompt or "\r" in self.prompt:
            return False

        return True

    def fix_prompt(self) -> str:
        """Fixes the prompt_continuation configuration variables."""
        if self.validate_prompt():
            return choose_config(self.console, self.prompt)
        self.console.print(
            f"[red]Prompt continuation invalid. {repr(self.prompt)} contains a "
            "newline character. Using default prompt continuation instead.[/red]"
        )
        return self.default_prompt
