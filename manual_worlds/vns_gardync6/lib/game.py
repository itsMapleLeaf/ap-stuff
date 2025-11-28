from typing import NotRequired, TypedDict


class GameData(TypedDict):
    # some game properties are actually required, but to keep things simple,
    # we'll treat the data/game.json file as the source of truth,
    # then these properties can serve as overrides
    game: NotRequired[str]
    creator: NotRequired[str]
    filler_item_name: NotRequired[str]
    starting_items: NotRequired[list["StartingItemData"]]
    death_link: NotRequired[bool]
    starting_index: NotRequired[int]


class StartingItemData(TypedDict):
    items: NotRequired[list[str]]
    item_categories: NotRequired[list[str]]
    random: NotRequired[int]
    if_previous_item: NotRequired[list[str]]
    yaml_option: NotRequired[list[str]]
