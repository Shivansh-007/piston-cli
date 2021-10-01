import json
import logging
import random
from pathlib import Path
from uuid import uuid4

import click
import requests
from requests_cache import CachedSession
from requests_cache.backends import FileCache
from rich.console import Console

from piston import __version__
from piston.utils.constants import (
    CACHE_LOCATION,
    REQUEST_CACHE_DURATION,
    REQUEST_CACHE_LOCATION,
    SPINNERS,
    PistonQuery,
)

log = logging.getLogger("rich")


def cache_query(payload: dict[str, ...]) -> str:
    """Create a normalized cache key from uuid and write `payload` to the CACHE with that filename."""
    key = uuid4()
    filename = Path(CACHE_LOCATION, f"{key}.json")
    filename.parent.mkdir(exist_ok=True)

    with open(filename, "w") as fp:
        json.dump(payload, fp)

    return filename.__str__()


def query_piston(ctx: click.Context, console: Console, payload: PistonQuery, cache_run: bool = False) -> dict:
    """Send a post request to the piston API with the code parameter."""
    http_session = CachedSession(
        # To avoid caching conflicts
        f"piston-v{__version__}",
        backend=FileCache(REQUEST_CACHE_LOCATION),
        expire_after=REQUEST_CACHE_DURATION,
    )

    output_json = {
        "language": payload.language,
        "source": payload.code,
        "args": payload.args,
        "stdin": payload.stdin,
    }
    location = None

    with console.status("Compiling", spinner=random.choice(SPINNERS)):
        logging.debug(f"Requests emkc v1 API with payload: {output_json}")
        try:
            return http_session.post(
                url="https://emkc.org/api/v1/piston/execute",
                data=json.dumps(output_json),
                timeout=3,
            ).json()
        except requests.exceptions.Timeout:
            if not cache_run:
                location = cache_query(output_json)
            console.print(
                "Connection timed out. Please check your connection and try again."
                f"Cached query saved at {location}"
                if location
                else ""
            )
            ctx.exit()
        except requests.exceptions.RequestException as e:
            if not cache_run:
                location = cache_query(output_json)
            console.print(
                f"Request raised exception: {e}\n" f"Cached query saved at {location}" if location else ""
            )
            ctx.exit()

    http_session.close()
