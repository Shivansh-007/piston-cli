import os
import platform
from typing import Optional

from piston.configuration.load_config import load_config
from piston.utilities.constants import Configuration
from rich.console import Console


def get_config(path: Optional[str]) -> dict:
    """Finds the configuration file path and loads the config at that location."""
    console = Console()

    if path:
        console.print(path)
        if os.path.isfile(path):
            console.print("[bold green]Loading configuration file![/bold green]")
            config = load_config(path)
            return config
        else:
            console.print(
                "[bold red]Error: No configuration file found at that location, "
                "using piston-cli defaults.[/bold red]"
            )
    else:
        path = Configuration.configuration_paths[platform.system()]
        console.print(path)
        if path is None:
            console.print(
                "[bold blue]Info: No default configuration location on your system, "
                "if you wish to use a configuration file, specify one with the --shell flag, "
                "loading piston-cli defaults.[/bold blue]"
            )
        else:
            if os.path.isfile(path):
                console.print("[bold green]Loading configuration file![/bold green]")
                config = load_config(path)
                return config
            else:
                console.print("foo")
                console.print(
                    "[bold blue]Info: No configuration file found at default location, "
                    "using piston-cli defaults.[/bold blue]"
                )

        return Configuration.default_configuration
