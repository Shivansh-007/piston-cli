import shlex
import typing as t


def parse_string(string: str) -> t.List[str]:
    """Parse string like python string parsing with the help of backslash."""
    parsed_string = shlex.shlex(string, posix=True)
    parsed_string.escapedquotes = "\"'"
    return list(parsed_string)
