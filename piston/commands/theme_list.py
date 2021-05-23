from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.python import Python3Lexer
from pygments.styles import get_style_by_name
from pygments.util import ClassNotFound

from piston.colorschemes import scheme_dict
from piston.utils.constants import CONSOLE, themes

with open("piston/utils/theme_preview.py", "r", encoding="utf-8") as f:
    code = f.read()


def theme_list() -> None:
    """List all available themes with a short code snippet."""
    for theme in themes:
        CONSOLE.print(f"[bold red underline]Theme {theme}: [/bold red underline]\n")
        try:
            style = get_style_by_name(theme)
        except ClassNotFound:
            style = scheme_dict[theme]
        finally:
            print(highlight(code, Python3Lexer(), Terminal256Formatter(style=style)))
