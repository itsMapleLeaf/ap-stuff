from typing import Any, Literal, TypedDict, NotRequired


class LocationArgs(TypedDict):
    category: NotRequired[str | list[str]]
    requires: NotRequired[str]
    region: NotRequired[str]
    place_item: NotRequired[list[str]]
    dont_place_item: NotRequired[list[str]]
    place_item_category: NotRequired[list[str]]
    dont_place_item_category: NotRequired[list[str]]
    victory: NotRequired[bool]
    prehint: NotRequired[bool]
    hint_entrance: NotRequired[str]
    id: NotRequired[int]


class LocationData(LocationArgs):
    name: str
