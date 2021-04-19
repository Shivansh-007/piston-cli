import sys

from requests.exceptions import ConnectionError

if not __package__:
    sys.path[0] = sys.path[0][: sys.path[0].rfind("/")]

import piston


if __name__ == "__main__":
    try:
        sys.exit(piston.main())
    except ConnectionError:
        print("\nUnable to establish a connection.")
    except Exception as e:
        print(f"Error: \n{e}")
    except KeyboardInterrupt:
        print("\nGoodbye!")
