from typing import NotRequired, TypedDict


class CategoryData(TypedDict):
    yaml_option: NotRequired[list[str]]
    hidden: NotRequired[bool]
