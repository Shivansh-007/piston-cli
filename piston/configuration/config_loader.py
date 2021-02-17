import os
import platform
from typing import Optional

from piston.utilities.constants import Configuration
from rich.console import Console
import yaml


class ConfigLoader:
    def __init__(self, path: Optional[str]):
        self.console = Console()
        self._path = Configuration.configuration_paths[platform.system()]
        if path is not None:
            self.set_path(path)
        self._config = {}

    def set_path(self, path: str):
        """Sets the path of private variable _path."""
        self._path = path

    def _load_yaml(self):
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

    def load_config(self):
        """Loads the configuration file."""
        if (
            not os.path.isfile(self._path)
            and self._path not in Configuration.configuration_paths.values()
        ):
            self.console.print(
                "[bold red]Error: No configuration file found at that location, "
                "using piston-cli defaults.[/bold red]"
            )
            return Configuration.default_configuration
        elif (
            not os.path.isfile(self._path)
            and self._path in Configuration.configuration_paths.values()
        ):
            self.console.print(
                "[bold blue]Info: No default configuration location on your system, "
                "if you wish to use a configuration file, specify one with the --shell flag, "
                "loading piston-cli defaults.[/bold blue]"
            )
            return Configuration.default_configuration

        self._load_yaml()

        return self._config
