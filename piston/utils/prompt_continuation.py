from piston.utils.constants import Shell


def prompt_continuation(*args) -> str:
    """Prompt continuation method for prompt_toolkit."""
    return Shell.prompt_continuation
