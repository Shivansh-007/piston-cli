import shlex
import typing as t


def split_unescape(string: str) -> t.List[str]:
    parsed_string = shlex.shlex(string, posix=True)
    parsed_string.escapedquotes = "\"'"
    return list(parsed_string)
