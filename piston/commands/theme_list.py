import click
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.python import Python3Lexer
from pygments.styles import get_style_by_name

from piston.utils.constants import THEME_PREVIEW, themes


def theme_list(ctx: click.Context) -> None:
    """List all available themes with a short code snippet."""
    for theme in themes:
        ctx.obj["console"].print(f"[bold red underline]Theme {theme}: [/bold red underline]\n")
        style = get_style_by_name(theme)
        print(highlight(THEME_PREVIEW, Python3Lexer(), Terminal256Formatter(style=style)))
