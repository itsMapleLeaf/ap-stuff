from typing import Any, Literal, TypedDict, NotRequired


class ItemArgs(TypedDict):
    category: NotRequired[str | list[str]]
    count: NotRequired[str | int]
    value: NotRequired[dict[str, int]]
    progression: NotRequired[bool]
    progression_skip_balancing: NotRequired[bool]
    useful: NotRequired[bool]
    trap: NotRequired[bool]
    filler: NotRequired[bool]
    early: NotRequired[bool | int]
    local: NotRequired[bool]
    local_early: NotRequired[bool | int]
    id: NotRequired[int]


class ItemData(ItemArgs):
    name: str
