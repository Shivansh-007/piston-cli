import os
import platform
from typing import Optional

import yaml
from piston.configuration.config_fixer import fix_config
from piston.utilities.constants import Configuration
from rich.console import Console


class ConfigLoader:
    """Loads yaml config files to customize piston-cli."""

    def __init__(self, path: Optional[str]):
        self.console = Console()
        self.path = path or Configuration.configuration_paths[platform.system()]
        self.config = {}

    def _load_yaml(self) -> None:
        """Loads the keys and values from a yaml file."""
        expandedpath = os.path.abspath(os.path.expandvars(self.path))

        self.console.print(f"[green]Loading config:[/green] {expandedpath}")

        with open(expandedpath) as loaded_config:
            loaded_config = yaml.load(loaded_config, Loader=yaml.FullLoader)

        for key, value in loaded_config.items():
            if key in Configuration.default_configuration:
                self.config[key] = value
                self.console.print(f"[green]- Loaded {key}(s): {value}[/green]")
            else:
                self.console.print(
                    f"[red]- Skipped {key}: {value} -- not a configurable value[/red]"
                )

        for key, value in Configuration.default_configuration.items():
            if key not in self.config:
                self.config[key] = value
                self.console.print(
                    f"[green]- Loaded default {key}: {value} -- not specified"
                )

    def load_config(self) -> dict:
        """Loads the configuration file."""
        if (
            not os.path.isfile(self.path)
            and self.path
            not in Configuration.configuration_paths.values()  # The config was likely passed
        ):
            self.console.print(
                "[bold red]Error: No configuration file found at that location or "
                "you are using a system with an unknown default configuration file location, "
                "loading piston-cli defaults.[/bold red]"
            )
            return Configuration.default_configuration
        elif (
            not os.path.isfile(self.path)
            and self.path
            in Configuration.configuration_paths.values()  # No config was passed - default config in use
        ):
            self.console.print(
                "[bold blue]Info: No default configuration file found on your system, "
                "loading piston-cli defaults.[/bold blue]"
            )
            return Configuration.default_configuration

        self._load_yaml()  # Set _config

        fix_config(self.config)  # Catch errors and fix the ones found

        return self.config
