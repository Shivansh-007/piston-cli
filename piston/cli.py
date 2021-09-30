import logging
from typing import Optional

import click
from more_itertools import grouper
from rich.console import Console

from piston import __version__, log
from piston._custom_click import DefaultCommandGroup
from piston.commands import Shell, run_file, run_link, theme_list
from piston.configuration.config_loader import ConfigLoader
from piston.utils import helpers
from piston.utils.compilers import languages_
from piston.utils.constants import BOX_STYLES, themes
from piston.utils.maketable import make_table

LIST_COMMANDS = {
    "themes": theme_list,
    "languages": ("Languages", grouper(languages_, 2)),
    "boxes": ("Box Styles", grouper(BOX_STYLES, 2)),
}
VALID_THEMES = [theme.lower() for theme in themes]


@click.group(
    cls=DefaultCommandGroup,
    context_settings=dict(help_option_names=["-h", "--help"]),
    invoke_without_command=True,
)
@click.version_option(version=__version__)
@click.option(
    "-t",
    "--theme",
    type=str,
    default=None,
    help="Change the default theme (solarized-dark) of code, to see available themes use -T or --theme-list",
)
@click.option(
    "--config",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        allow_dash=False,
        path_type=str,
    ),
    is_eager=True,
    help=(
        "Path to the piston-cli config file, "
        "leave blank if your config is in the system default location specified in the README"
    ),
)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode")
@click.pass_context
def cli_app(
    ctx: click.Context,
    verbose: bool,
    theme: Optional[str],
    config: Optional[str],
) -> None:
    log.setup(logging.DEBUG if verbose else logging.INFO)

    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    console = Console()
    config_loader = ConfigLoader(console, config)
    ctx.obj["config"] = config_loader.load_config()
    ctx.obj["theme"] = theme or ctx.obj["config"]["theme"]
    ctx.obj["console"] = console

    if theme:
        ctx.obj["console"].print(
            f"[indian_red]- Theme flag specified, overwriting theme loaded from "
            f"config: {theme}[/indian_red]"
        )


@cli_app.command("theme-list")
@click.argument(
    "value",
    type=click.Choice([t.lower() for t in LIST_COMMANDS.keys()]),
    required=True,
)
@click.pass_context
def cli_theme_list(ctx: click.Context, value: str) -> None:
    try:
        # If the value is an tuple i.e. it is formatted for a box.
        if isinstance(LIST_COMMANDS[value], tuple):
            table = make_table(*LIST_COMMANDS[value])
            ctx.obj["console"].print(table)
        else:
            # Else it is just a callable and we can call it.
            LIST_COMMANDS[value](ctx)
    except KeyError:
        ctx.obj["console"].print(
            f"[red] Invalid option provided - Valid "
            f"options include:[/red] [cyan]{', '.join(LIST_COMMANDS.keys())}[/cyan]"
        )


@cli_app.command("file")
@click.argument(
    "src",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True, allow_dash=True),
    is_eager=True,
    required=True,
)
@click.pass_context
def cli_file(ctx: click.Context, src: str) -> None:
    config = ctx.obj["config"]

    output = run_file(ctx, src)
    ctx.obj["console"].print(f"\nHere is your output for {src}:")
    ctx.obj["console"].print(
        helpers.print_msg_box(
            output,
            style=config["box_style"],
        )
    )


@cli_app.command("pastebin")
@click.argument(
    "link",
    type=str,
    required=True,
)
@click.option(
    "--language",
    type=str,
    required=True,
)
@click.pass_context
def cli_pastebin(ctx: click.Context, link: str, language: str) -> None:
    config = ctx.obj["config"]

    output = run_link(ctx, link, language)
    ctx.obj["console"].print(f"\nHere is your {language} output:")
    ctx.obj["console"].print(
        helpers.print_msg_box(
            output,
            style=config["box_style"],
        )
    )


@cli_app.command("shell")
@click.argument(
    "language",
    type=str,
    required=True,
)
@click.pass_context
def cli_shell(ctx: click.Context, language: str) -> None:
    config = ctx.obj["config"]

    Shell(ctx).run_shell(
        language,
        ctx.obj["theme"],
        config["prompt_start"],
        config["prompt_continuation"],
    )


@cli_app.command(default_command=True)
@click.argument(
    "src",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True, allow_dash=True),
    is_eager=True,
    required=True,
)
@click.argument("args", nargs=-1)
@click.pass_context
def cli_interpreter(ctx: click.Context, src: str, args: tuple[str]) -> None:
    config = ctx.obj["config"]

    output = run_file(ctx, src, list(args))
    ctx.obj["console"].print(f"\nHere is your output for {src}:")
    ctx.obj["console"].print(
        helpers.print_msg_box(
            output,
            style=config["box_style"],
        )
    )
