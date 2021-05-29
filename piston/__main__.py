import sys
from signal import SIGINT, signal

if not __package__:
    sys.path[0] = sys.path[0][: sys.path[0].rfind("/")]

import piston
from piston.utils.helpers import signal_handler

if __name__ == "__main__":
    # Listen for SIGINT
    signal(SIGINT, signal_handler)

    try:
        sys.exit(piston.main())
    except Exception as e:
        print(f"Error: \n{e}")
