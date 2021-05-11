import sys

if not __package__:
    sys.path[0] = sys.path[0][: sys.path[0].rfind("/")]

import piston


if __name__ == "__main__":
    try:
        sys.exit(piston.main())
    except KeyboardInterrupt:
        sys.exit("\nGoodbye!")
    except Exception as e:
        print(f"Error: \n{e}")
