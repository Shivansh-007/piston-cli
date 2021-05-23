from piston.configuration.choose_config import choose_config
from piston.utilities.constants import Configuration
from piston.configuration.validators.validator_base import Validator


class PromptStartValidator(Validator):
    """Validates the prompt_start config variable"""

    def __init__(self, prompt: str) -> None:
        self.prompt = prompt
        self.default_prompt = Configuration.default_configuration["prompt_start"]
        super().__init__(self.prompt, self.default_prompt, "prompt_start")

    def validate_prompt(self) -> bool:
        if not self.validate_type():
            return False

        # Make sure there are no new lines in the prompt
        if "\n" in self.prompt or "\r" in self.prompt:
            return False

        return True

    def fix_prompt(self) -> str:
        if self.validate_prompt():
            return choose_config(self.prompt)
        return self.default_prompt


class PromptContinuationValidator(Validator):
    """Validates the prompt_continuation config variable"""

    def __init__(self, prompt: str) -> None:
        self.prompt = prompt
        self.default_prompt = Configuration.default_configuration["prompt_continuation"]
        super().__init__(self.prompt, self.default_prompt, "prompt_continuation")

    def validate_prompt(self) -> bool:
        if not self.validate_type():
            return False

        # Make sure there are no new lines in the prompt
        if "\n" in self.prompt or "\r" in self.prompt:
            return False

        return True

    def fix_prompt(self) -> str:
        if self.validate_prompt():
            return choose_config(self.prompt)
        return self.default_prompt
