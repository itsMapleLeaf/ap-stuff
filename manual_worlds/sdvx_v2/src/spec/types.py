from typing import Any, Literal, TypedDict, NotRequired


class CategoryData(TypedDict):
    yaml_option: NotRequired[list[str]]
    hidden: NotRequired[bool]


class StartingItemData(TypedDict):
    items: NotRequired[list[str]]
    item_categories: NotRequired[list[str]]
    random: NotRequired[int]
    if_previous_item: NotRequired[list[str]]
    yaml_option: NotRequired[list[str]]


class GameData(TypedDict):
    # some game properties are actually required, but to keep things simple,
    # we'll treat the data/game.json file as the source of truth,
    # then these properties can serve as overrides
    game: NotRequired[str]
    creator: NotRequired[str]
    filler_item_name: NotRequired[str]
    starting_items: NotRequired[list[StartingItemData]]
    death_link: NotRequired[bool]
    starting_index: NotRequired[int]


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


class LocationTableData(TypedDict):
    schema: NotRequired[str]
    data: NotRequired[list[LocationData]]


class RegionData(TypedDict):
    requires: NotRequired[str]
    connects_to: NotRequired[list[str]]
    starting: NotRequired[bool]
    exit_requires: NotRequired[dict[str, str]]
    entrance_requires: NotRequired[dict[str, str]]


class TutorialData(TypedDict):
    name: str
    description: str
    language: str
    file_name: str
    link: NotRequired[str]
    authors: NotRequired[list[str]]


class WebData(TypedDict):
    options_page: NotRequired[bool | str]
    game_info_languages: NotRequired[list[str]]
    theme: NotRequired[str]
    bug_report_page: NotRequired[str]
    tutorials: NotRequired[list[TutorialData]]
    options_presets: NotRequired[dict[str, dict[str, Any]]]


class DocsData(TypedDict):
    apworld_description: NotRequired[list[str]]
    web: NotRequired[WebData]


class MetaData(TypedDict):
    docs: NotRequired[DocsData]
    enable_region_diagram: NotRequired[bool]


class BaseOptionData(TypedDict):
    display_name: NotRequired[str]
    description: NotRequired[str | list[str]]
    rich_text_doc: NotRequired[bool]
    group: NotRequired[str]
    hidden: NotRequired[bool]
    visibility: NotRequired[str | list[str] | int]


class ToggleOptionData(BaseOptionData):
    type: Literal["Toggle"]
    default: bool


class ChoiceOptionData(BaseOptionData):
    type: Literal["Choice"]
    values: dict[str, int]
    aliases: NotRequired[dict[str, int | str]]
    default: NotRequired[int]
    allow_custom_value: NotRequired[bool]


class RangeOptionData(BaseOptionData):
    type: Literal["Range"]
    range_start: NotRequired[int]
    range_end: NotRequired[int]
    default: NotRequired[int]
    values: NotRequired[dict[str, int]]


class CoreOptionData(BaseOptionData):
    default: NotRequired[int | bool]
    aliases: NotRequired[dict[str, int | str]]
    values: NotRequired[dict[str, int]]


type UserOptionData = ToggleOptionData | ChoiceOptionData | RangeOptionData


class OptionTableData(TypedDict):
    core: NotRequired[dict[str, CoreOptionData]]
    user: NotRequired[dict[str, UserOptionData]]
