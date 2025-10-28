from typing import Any, Literal, TypedDict, NotRequired


class CategoryData(TypedDict):
    yaml_option: NotRequired[list[str]]
    hidden: NotRequired[bool]
