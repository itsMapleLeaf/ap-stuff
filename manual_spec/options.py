from typing import Literal, TypedDict, NotRequired


class BaseOptionData(TypedDict):
    display_name: NotRequired[str]
    description: NotRequired[str | list[str]]
    rich_text_doc: NotRequired[bool]
    group: NotRequired[str]
    hidden: NotRequired[bool]
    visibility: NotRequired[str | list[str] | int]


class ToggleOptionArgs(BaseOptionData):
    default: bool


class ToggleOptionData(ToggleOptionArgs):
    type: Literal["Toggle"]


class ChoiceOptionArgs(BaseOptionData):
    values: dict[str, int]
    aliases: NotRequired[dict[str, int | str]]
    default: NotRequired[int]
    allow_custom_value: NotRequired[bool]


class ChoiceOptionData(ChoiceOptionArgs):
    type: Literal["Choice"]


class RangeOptionArgs(BaseOptionData):
    range_start: NotRequired[int]
    range_end: NotRequired[int]
    default: NotRequired[int]
    values: NotRequired[dict[str, int]]


class RangeOptionData(RangeOptionArgs):
    type: Literal["Range"]


class CoreOptionData(BaseOptionData):
    default: NotRequired[int | bool]
    aliases: NotRequired[dict[str, int | str]]
    values: NotRequired[dict[str, int]]


type UserOptionData = ToggleOptionData | ChoiceOptionData | RangeOptionData
