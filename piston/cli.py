import glob
import json
import logging
import os
import random
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
from piston.utils.constants import BOX_STYLES, CACHE_LOCATION, SPINNERS, PistonQuery, themes
from piston.utils.maketable import make_table
from piston.utils.services import query_piston

LIST_COMMANDS = {
    "themes": theme_list,
    "languages": ("Languages", grouper(languages_, 2)),
    "boxes": ("Box Styles", grouper(BOX_STYLES, 2)),
}
VALID_THEMES = [theme.lower() for theme in themes]


@click.group(
    cls=DefaultCommandGroup,
    context_settings=dict(help_option_names=["-h", "--help"], max_content_width=400),
    invoke_without_command=True,
)
@click.version_option(version=__version__)
@click.option(
    "-t",
    "--theme",
    type=str,
    default=None,
    help=(
        "Set the theme for syntax highlighting. Use 'piston list themes' to"
        "see all available themes. To set a default theme, add the"
        "'theme=\"...\"' option to the configuration file"
    ),
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
    """
    Piston CLI!

    It is a universal shell supporting code highlighting, files, interpretation and a lot more without the
    need to download a language.

    -- Default Command
    If no commands are specified, it by default runs the interpreter command, this feature allows piston to
    act like an interpreter, the design of this is inspired from python. For example:

    Instead of calling `python code.rb a b c d` you can call --> `piston python code.rb a b c d`
    """
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


@cli_app.command("list")
@click.argument(
    "value",
    type=click.Choice([t.lower() for t in LIST_COMMANDS.keys()]),
    required=True,
)
@click.pass_context
def cli_list(ctx: click.Context, value: str) -> None:
    """Display the list of <value> supported by piston-cli."""
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
    """Run code from the specified file."""
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
    help=(
        "Set the language for running the piston query (pastebins aren't accurate). The language can be "
        "specified as a name (like 'C++' or 'python'). Use 'piston list languages' to show all "
        "supported language names."
    ),
)
@click.pass_context
def cli_pastebin(ctx: click.Context, link: str, language: str) -> None:
    """Run code from a pastebin link, currently only paste.pythondiscord.com is supported."""
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
    """
    Run code in a shell, just like the place you are running this command from.

    With continuous support for the supported language.
    """
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
    """
    This allows piston to act like an interpreter, the design of this is inspired from python. For example.

    Instead of calling `python code.rb a b c d` you can call --> `piston python code.rb a b c d`
    """
    config = ctx.obj["config"]

    output = run_file(ctx, src, list(args))
    ctx.obj["console"].print(f"\nHere is your output for {src}:")
    ctx.obj["console"].print(
        helpers.print_msg_box(
            output,
            style=config["box_style"],
        )
    )


@cli_app.command("cache")
@click.argument(
    "timeline",
    default=1,
    type=int,
    required=False,
)
@click.option(
    "--cache-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True, allow_dash=True),
    is_eager=True,
    required=False,
    help=(
        "Sometimes, you don't remember how long back in timeline was the cache file, or you want to run a"
        " specific JSON file. This option makes this possible. For example:"
        "\n\n$ piston cache --cache-file ~/.cache/piston-cli/cachefile.json"
    ),
)
@click.option("--clear-cache", is_flag=True, help="Clear piston-cli cache")
@click.option("--cache-path", is_flag=True, help="Show piston-cli cache path")
@click.pass_context
def cli_failed_request_cache(
    ctx: click.Context, timeline: int, clear_cache: bool, cache_path: bool, cache_file: Optional[str] = None
) -> None:
    """
    This command allows you to run cached piston-cli queries.

    In case of connection timeout, or network connection relation problems, piston-cli stores
    the query which is being sent to the piston API in cache, currently this is default according
    to the operating system and cannot be changed. You can view the path of the caching directory
    by specifying **--cache-path** option to this command, remember not the root cli group.

    Just got back your internet, and want to run your last piston-cli query. You can use the timeline argument
    it allows you to specify the 'timeline' of the query you want to run, say you want to run your second last
    query, remember this is in respect of request error queries, you can specify it as `2`. For example:

    $ piston cache 2
    """
    config = ctx.obj["config"]
    cache_glob = glob.glob(str(CACHE_LOCATION) + "/*")
    console = ctx.obj["console"]

    if cache_path:
        console.print(
            f"[blue]Your piston-cli cache is stored at "
            f"[link={CACHE_LOCATION.as_uri()}]{CACHE_LOCATION}[/]"
        )
        ctx.exit()

    if clear_cache:
        with console.status("Aye Aye! Cleaning your cache", spinner=random.choice(SPINNERS)):
            for f in cache_glob:
                os.remove(f)
        console.print("[blue]Your cache has been clean![/]")
        ctx.exit()

    ordered_cache_files = list(cache_glob)
    ordered_cache_files = [file for file in ordered_cache_files if file.endswith(".json")]
    ordered_cache_files.sort(key=lambda x: os.path.getmtime(x))

    cache_file = cache_file or ordered_cache_files[timeline - 1]  # Python has zero-based indexing

    with open(cache_file, "r") as fp:
        data = json.load(fp)

    query = PistonQuery(data["language"], data["source"], data["args"], data["stdin"])
    data = query_piston(ctx, console, query, cache_run=True)
    output = [data["output"].split("\n"), "Your code ran without output."][len(data["output"]) == 0]

    console.print(f"\nHere is your output for {cache_file.__str__()}:")
    console.print(
        helpers.print_msg_box(
            output,
            style=config["box_style"],
        )
    )
