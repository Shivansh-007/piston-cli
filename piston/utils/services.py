import json
import logging
import random
import sys

import requests
from requests_cache import CachedSession
from requests_cache.backends import FileCache
from rich.console import Console

from piston import __version__
from piston.utils.constants import REQUEST_CACHE_DURATION, REQUEST_CACHE_LOCATION, SPINNERS, PistonQuery

log = logging.getLogger("rich")


def query_piston(console: Console, payload: PistonQuery) -> dict:
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

    with console.status("Compiling", spinner=random.choice(SPINNERS)):
        logging.debug(f"Requests emkc v1 API with payload: {output_json}")
        try:
            return http_session.post(
                url="https://emkc.org/api/v1/piston/execute",
                data=json.dumps(output_json),
                timeout=3,
            ).json()
        except requests.exceptions.Timeout:
            sys.exit("Connection timed out. Please check your connection and try again.")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    http_session.close()
