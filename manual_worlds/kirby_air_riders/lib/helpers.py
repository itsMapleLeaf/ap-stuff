from typing import Union, Unpack


def range_inclusive(start_or_len: int, end_arg: int | None = None):
    match (start_or_len, end_arg):
        case (start, int(end)):
            pass
        case (len, None):
            start, end = 0, len

    for i in range(start, end):
        yield i + 1
