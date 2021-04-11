import os
import platform
from typing import Optional, Union

import yaml

from piston.configuration.config_fixer import fix_config
from piston.utils.constants import CONSOLE, Configuration


class ConfigLoader:
    """Loads yaml config files to customize piston-cli."""

    def __init__(self, paths: Optional[Union[str, tuple]]):
        if paths:
            self.paths = paths
        elif platform.system() in Configuration.configuration_paths:
            self.paths = Configuration.configuration_paths[platform.system()]
        self.config = {}

    def _load_yaml(self) -> None:
        """Loads the keys and values from a yaml file."""
        expanded_path = os.path.abspath(os.path.expandvars(self.paths))

        CONSOLE.print(f"[green]Loading config:[/green] {expanded_path}")

        with open(expanded_path) as loaded_config:
            loaded_config = yaml.load(loaded_config, Loader=yaml.FullLoader)

        for key, value in loaded_config.items():
            if key in Configuration.default_configuration:
                self.config[key] = value
                CONSOLE.print(f"[green]- Loaded {key}(s): {value}[/green]")
            else:
                CONSOLE.print(
                    f"[red]- Skipped {key}: {value} -- not a configurable value[/red]"
                )

        for key, value in Configuration.default_configuration.items():
            if key not in self.config:
                self.config[key] = value
                CONSOLE.print(
                    f"[green]- Loaded default {key}: {value} -- not specified"
                )

    def load_config(self) -> dict:
        """Loads the configuration file."""
        path_exists = False

        if isinstance(self.paths, str):
            if os.path.isfile(self.paths):
                path_exists = True
        elif isinstance(self.paths, tuple):
            for path in self.paths:
                if os.path.isfile(path):
                    path_exists = True
                    self.paths = path
                    break

        if path_exists:
            CONSOLE.print(
                "[blue]One or more configuration files were found to exist. "
                f"Using the one found at {self.paths}."
            )

        if (
            not path_exists
            and self.paths
            # The path is not in a default location,
            # this means that it is None from an unrecognized system or was manually specified
            not in Configuration.configuration_paths.values()
        ):
            CONSOLE.print(
                "[bold red]Error: No configuration file found at that location or "
                "you are using a system with an unknown default configuration file location, "
                "loading piston-cli defaults.[/bold red]"
            )
            return Configuration.default_configuration
        elif (
            # The path is in a default location, a path was probably not specified,
            # unless the user pointed to one in the default location
            not path_exists
            and self.paths in Configuration.configuration_paths.values()
        ):
            CONSOLE.print(
                "[bold blue]Info: No default configuration file found on your system, "
                "loading piston-cli defaults.[/bold blue]"
            )
            return Configuration.default_configuration

        self._load_yaml()  # Set config

        fix_config(self.config)  # Catch errors and fix the ones found

        return self.config
