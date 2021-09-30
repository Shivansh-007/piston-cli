import os
from typing import Optional, Union

import rich
import yaml

from piston.configuration.config_fixer import fix_config
from piston.utils.constants import Configuration


class ConfigLoader:
    """Loads yaml config files to customize piston-cli."""

    def __init__(self, console: rich.console.Console, paths: Optional[Union[str, tuple]]):
        self.console = console
        if paths:
            self.paths = paths
        else:
            self.paths = Configuration.configuration_path
        self.config = {}

        self.path_loaded = None

    def _load_yaml(self) -> None:
        """Loads the keys and values from a yaml file."""
        expanded_path = os.path.abspath(os.path.expandvars(self.path_loaded))

        self.console.print(f"[green]Loading config:[/green] {expanded_path}")

        with open(expanded_path) as loaded_config:
            loaded_config = yaml.load(loaded_config, Loader=yaml.FullLoader)  # noqa: S506

        for key, value in loaded_config.items():
            if key in Configuration.default_configuration:
                self.config[key] = value
                self.console.print(f"[green]- Loaded {key}(s): {value}[/green]")
            else:
                self.console.print(f"[red]- Skipped {key}: {value} -- not a configurable value[/red]")

        for key, value in Configuration.default_configuration.items():
            if key not in self.config:
                self.config[key] = value
                self.console.print(f"[green]- Loaded default {key}: {value} -- not specified")

    def load_config(self) -> dict:
        """Loads the configuration file."""
        existing_paths = []

        if isinstance(self.paths, str):
            if os.path.isfile(self.paths):
                existing_paths.append(self.paths)
        elif isinstance(self.paths, tuple):
            for path in self.paths:
                if os.path.isfile(path):
                    existing_paths.append(path)

        if len(existing_paths) > 1:
            self.console.print(
                "[blue]One or more configuration files were found to exist. "
                f"Using the one found at {existing_paths[0]}."
            )

        if (
            not existing_paths
            # The path is not in a default location,
            # this means that it is None from an unrecognized system or was manually specified
            and self.paths not in Configuration.configuration_path
        ):
            self.console.print(
                "[bold red]Error: No configuration file found at that location or "
                "you are using a system with an unknown default configuration file location, "
                "loading piston-cli defaults.[/bold red]"
            )
            return Configuration.default_configuration

        elif (
            # The path is in a default location, a path was probably not specified,
            # unless the user pointed to one in the default location
            not existing_paths
            and self.paths in Configuration.configuration_path
        ):
            self.console.print(
                "[bold blue]Info: No default configuration file found on your system, "
                "loading piston-cli defaults.[/bold blue]"
            )
            return Configuration.default_configuration

        # Choose the first path which is loaded
        self.path_loaded = existing_paths[0]

        self._load_yaml()  # Set config
        fix_config(self.console, self.config)  # Catch errors and fix the ones found

        return self.config
