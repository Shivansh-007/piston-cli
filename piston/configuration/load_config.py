import yaml
from piston.utilities.constants import Configuration
from rich.console import Console


def load_config(path: str) -> dict:
    """Loads the keys and values from a configuration file."""
    console = Console()

    with open(path) as config:
        config = yaml.load(config, Loader=yaml.FullLoader)

    out = {}
    for key in config:
        if key in Configuration.default_configuration:
            out[key] = config[key]
            console.print(f"[green]- Loaded {key}: {config[key]}[/green]")
        else:
            console.print(
                f"[red]- Skipping {key}: {config[key]} -- not a configurable value[/red]"
            )

    for key in Configuration.default_configuration:
        if key not in out:
            out[key] = Configuration.default_configuration[key]

    return out
