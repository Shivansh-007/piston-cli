from piston.utilities.constants import Configuration, console, themes


def validate_theme(theme: str) -> bool:
    """Validates a theme string."""
    current_type = type(theme)
    target_type = type(Configuration.default_configuration["theme"])
    if current_type is not target_type:
        console.print(
            f"[red]Theme invalid, use type {target_type.__name__}, "
            f"not {current_type.__name__}. Using default theme.[/red]"
        )
        return False
    if theme not in themes:
        console.print(
            f'[red]Theme invalid, "{theme}" not recognized. Using default theme.[/red]'
        )
        return False
    return True
