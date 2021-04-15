from typing import Union

from piston.configuration.choose_config import choose_config
from piston.configuration.validators.validator_base import Validator
from piston.utils.constants import CONSOLE, Configuration, boxes


class MessageBoxValidator(Validator):
    """Validates a string or list of message box styles by checking multiple criteria."""

    def __init__(self, message_boxes: Union[str, list]) -> None:
        self.message_boxes = message_boxes
        self.default_box = Configuration.default_configuration["message_box"]
        super().__init__(message_boxes, self.default_box, "message_box")

    @staticmethod
    def check_box_exists(box: str) -> bool:
        """Ensures that a given message box exists."""
        if box not in boxes:
            CONSOLE.print(
                f'[red]Message Box invalid, "{box}" not recognized. Using default message box.[/red]'
            )
            return False
        return True

    def validate_box(self) -> bool:
        """Validates a message box string."""
        if not self.validate_type():
            return False

        # Check the singular message box exists.
        if isinstance(self.message_boxes, str) and not self.check_box_exists(
            self.message_boxes
        ):
            return False

        if isinstance(self.message_boxes, list):  # Check each message box exists.
            for box in self.message_boxes:
                if not self.check_box_exists(box):
                    return False

        return True

    def fix_box_style(self) -> str:
        """Finds and corrects any errors in a given box or list of boxes, then returns a fixed version."""
        if self.validate_box():
            return choose_config(self.message_boxes)
        return self.default_box
