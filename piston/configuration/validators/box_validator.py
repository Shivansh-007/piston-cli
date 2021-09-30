from typing import Union

import rich

from piston.configuration.choose_config import choose_config
from piston.configuration.validators.validator_base import Validator
from piston.utils.constants import BOX_STYLES, Configuration


class BoxStyleValidator(Validator):
    """Validates a string or list of box styles by checking multiple criteria."""

    def __init__(self, console: rich.console.Console, box_styles: Union[str, list]) -> None:
        self.console = console
        self.box_styles = box_styles
        self.default_box = Configuration.default_configuration["box_style"]
        super().__init__(console, box_styles, self.default_box, "box_style")

    def check_box_exists(self, box: str) -> bool:
        """Ensures that a given box style exists."""
        if box not in BOX_STYLES:
            self.console.print(
                f'[red]Box Style invalid, "{box}" not recognized. Using default box style.[/red]'
            )
            return False
        return True

    def validate_box_style(self) -> bool:
        """Validates box styles."""
        if not self.validate_type():
            return False

        # Check the singular box style exists.
        if isinstance(self.box_styles, str) and not self.check_box_exists(self.box_styles):
            return False

        if isinstance(self.box_styles, list):  # Check each box style exists.
            for box in self.box_styles:
                if not self.check_box_exists(box):
                    return False

        return True

    def fix_box_style(self) -> str:
        """Finds and corrects any errors in a given box or list of boxes, then returns a fixed version."""
        if self.validate_box_style():
            return choose_config(self.console, self.box_styles)
        return self.default_box
