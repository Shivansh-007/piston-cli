import logging
import os
import sys
from logging import handlers
from pathlib import Path

import coloredlogs
from appdirs import user_cache_dir


def setup(log_level: int = logging.INFO) -> None:
    """Set up loggers."""
    log_file = Path(user_cache_dir("piston-cli"), "piston.log")
    log_file.parent.mkdir(exist_ok=True)

    format_string = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    log_format = logging.Formatter(format_string)
    file_handler = handlers.RotatingFileHandler(log_file, maxBytes=5242880, backupCount=7, encoding="utf8")
    file_handler.setFormatter(log_format)

    root_log = logging.getLogger()
    root_log.setLevel(log_level)
    root_log.addHandler(file_handler)

    if "COLOREDLOGS_LEVEL_STYLES" not in os.environ:
        coloredlogs.DEFAULT_LEVEL_STYLES = {
            **coloredlogs.DEFAULT_LEVEL_STYLES,
            "critical": {"background": "red"},
            "debug": {"color": "blue"},
        }

    if "COLOREDLOGS_LOG_FORMAT" not in os.environ:
        coloredlogs.DEFAULT_LOG_FORMAT = format_string

    if "COLOREDLOGS_LOG_LEVEL" not in os.environ:
        coloredlogs.DEFAULT_LOG_LEVEL = log_level

    logging.getLogger("requests_cache").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    # Set back to the default of INFO even if asyncio's debug mode is enabled.
    logging.getLogger("asyncio").setLevel(logging.INFO)

    coloredlogs.install(logger=root_log, stream=sys.stdout)
