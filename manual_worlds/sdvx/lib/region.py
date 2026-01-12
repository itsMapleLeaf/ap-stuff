from typing import Any, Literal, TypedDict, NotRequired


class RegionData(TypedDict):
    requires: NotRequired[str]
    connects_to: NotRequired[list[str]]
    starting: NotRequired[bool]
    exit_requires: NotRequired[dict[str, str]]
    entrance_requires: NotRequired[dict[str, str]]
