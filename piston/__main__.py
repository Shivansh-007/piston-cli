import sys
from signal import SIGINT, signal

if not __package__:
    sys.path[0] = sys.path[0][: sys.path[0].rfind("/")]

from piston import cli
from piston.utils.helpers import signal_handler

if __name__ == "__main__":
    signal(SIGINT, signal_handler)
    cli.cli_app()
