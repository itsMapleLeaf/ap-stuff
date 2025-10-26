from pathlib import Path
import sys


class ArgsOverride:
    """
    A context manager that temporarily overrides sys.argv with custom arguments.

    This class is useful for testing or running code that depends on command-line
    arguments without actually modifying the global sys.argv permanently.

    Args:
        *args (str | Path): Variable number of arguments to use as sys.argv override.
            These will be converted to strings and appended after the program name.

    Attributes:
        args (list[str]): List of arguments converted to strings.
        old_argv (list[str]): Backup of the original sys.argv (set on __enter__).

    Example:
        >>> with ArgsOverride('--flag', 'value', Path('/some/path')):
        ...     # sys.argv is now ['program_name', '--flag', 'value', '/some/path']
        ...     parse_arguments()
        >>> # sys.argv is restored to original value
    """

    def __init__(self, *args: str | Path) -> None:
        self.args = list(map(str, args))

    def __enter__(self):
        self.old_argv = sys.argv[:]
        sys.argv = self.old_argv[0:1] + self.args

    def __exit__(self, type, value, traceback):
        sys.argv = self.old_argv[:]
