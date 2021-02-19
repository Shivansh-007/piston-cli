import os
import platform
from typing import Optional

import yaml
from piston.configuration.config_validator import validate_config
from piston.utilities.constants import Configuration
from rich.console import Console


class ConfigLoader:
    """Loads yaml config files to customize piston-cli."""

    def __init__(self, path: Optional[str]):
        self.console = Console()
        self._path = Configuration.configuration_paths[platform.system()]
        if path is not None:
            self.set_path(path)
        self._config = {}

    def set_path(self, path: str) -> None:
        """Sets the path of private variable _path."""
        self._path = path

    def _load_yaml(self) -> None:
        """Loads the keys and values from a yaml file."""
        expanded_path = os.path.abspath(os.path.expandvars(self._path))

        self.console.print(f"[green]Loading config:[/green] {expanded_path}")

        with open(expanded_path) as loaded_config:
            loaded_config = yaml.load(loaded_config, Loader=yaml.FullLoader)

        for key, value in loaded_config.items():
            if key in Configuration.default_configuration:
                self._config[key] = value
                self.console.print(f"[green]- Loaded {key}: {value}[/green]")
            else:
                self.console.print(
                    f"[red]- Skipped {key}: {value} -- not a configurable value[/red]"
                )

        for key, value in Configuration.default_configuration.items():
            if key not in self._config:
                self._config[key] = value
                self.console.print(
                    f"[green]- Loaded default {key}: {value} -- not specified"
                )

    def load_config(self) -> dict:
        """Loads the configuration file."""
        if (
            not os.path.isfile(self._path)
            and self._path not in Configuration.configuration_paths.values()  # The config path was explicitly passed or the user is using a system with an unkown default config file location (currently on Java virtual machines)
        ):
            self.console.print(
                "[bold red]Error: No configuration file found at that location or you are using a system with an unknown default configuration file location, "
                "loading piston-cli defaults.[/bold red]"
            )
            return Configuration.default_configuration
        elif (
            not os.path.isfile(self._path)
            and self._path in Configuration.configuration_paths.values()  # No congfig was explicitly passed.
        ):
            self.console.print(
                "[bold blue]Info: No default configuration file found on your system, "
                "loading piston-cli defaults.[/bold blue]"
            )
            return Configuration.default_configuration

        self._load_yaml() # Set _config

        validate_config(self._config) # Catch errors and fix the ones found

        return self._config
