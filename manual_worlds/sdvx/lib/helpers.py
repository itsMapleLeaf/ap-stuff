from typing import TYPE_CHECKING, Union, Unpack, cast
from Options import Option
from ..Helpers import get_option_value

if TYPE_CHECKING:
    from BaseClasses import MultiWorld


def range_inclusive(start_or_len: int, end_arg: int | None = None):
    match (start_or_len, end_arg):
        case (start, int(end)):
            pass
        case (len, None):
            start, end = 0, len

    for i in range(start, end):
        yield i + 1


def option_value_of[T](
    multiworld: "MultiWorld",
    player: int,
    option_class: type[Option[T]],
    option_name: str | None = None,
) -> T:
    resolved_option_name = option_name
    if resolved_option_name is None:
        if not hasattr(option_class, "name"):
            raise ValueError(
                "option_name must be provided if option_class has no 'name' attribute"
            )
        resolved_option_name = getattr(option_class, "name")

    return cast(
        T,
        get_option_value(multiworld, player, resolved_option_name),
    )
