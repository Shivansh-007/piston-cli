import json
from typing import Optional, Tuple

import requests

MAX_PASTE_LEN = 10000
FAILED_REQUEST_ATTEMPTS = 3
MAX_LINES = 20
MAX_CHARACTERS = 2000


def format_output(output: str) -> Tuple[str, Optional[str]]:
    """
    Format the output and return a tuple of the formatted output and a URL to the full output.

    Prepend each line with a line number. Truncate if there are over MAX_LINES lines or
    MAX_CHARACTERS characters and upload the full output to a paste service.
    """
    output = output.rstrip("\n")
    original_output = output  # To be uploaded to a pasting service if needed
    paste_link = None
    truncated = False
    lines = output.count("\n")

    if lines > 0:
        output = [f"{i:03d} | {line}" for i, line in enumerate(output.split("\n"), 1)]
        output = output[:MAX_LINES]  # Limiting to only 20 lines
        output = "\n".join(output)

    if lines > MAX_LINES:
        truncated = True
        if len(output) >= MAX_CHARACTERS:
            output = (
                f"{output[:MAX_CHARACTERS]}\n... (truncated - too long, too many lines)"
            )
        else:
            output = f"{output}\n... (truncated - too many lines)"
    elif len(output) >= MAX_CHARACTERS:
        truncated = True
        output = f"{output[:MAX_CHARACTERS]}\n... (truncated - too long)"

    if truncated:
        paste_link = upload_output(original_output)

    output = output or "[No output]"

    return output, paste_link


def upload_output(output: str) -> Optional[str]:
    """Upload the eval output to a paste service and return a URL to it if successful."""
    if len(output) > MAX_PASTE_LEN:
        return "too long to upload"
    return send_to_paste_service(output, extension="txt")


def send_to_paste_service(contents: str, *, extension: str = "") -> Optional[str]:
    """
    Upload `contents` to the paste service.

    `extension` is added to the output URL
    When an error occurs, `None` is returned, otherwise the generated URL with the suffix.
    """
    upload_url = "https://emkc.org/snippets"
    for _ in range(FAILED_REQUEST_ATTEMPTS):
        payload = json.dumps(
            {
                "language": "txt",
                "snip": contents,
            }
        )

        response = requests.post(upload_url, data=payload)
        if response.status_code == 200:
            response = response.json()
            return "https://emkc.org" + response["url"]
