from typing import Unpack

from .meta import MetaData
from .options import (
    ChoiceOptionArgs,
    ChoiceOptionData,
    CoreOptionData,
    RangeOptionArgs,
    RangeOptionData,
    RangeOptionSpec,
    ToggleOptionArgs,
    ToggleOptionData,
    ToggleOptionSpec,
    UserOptionData,
)
from .region import RegionData
from .category import CategoryData
from .game import GameData
from .location import LocationData, LocationArgs
from .item import ItemData, ItemArgs


class WorldSpec:
    def __init__(self, **game: Unpack[GameData]):
        self.game: GameData = game
        self.items: dict[str, ItemData] = {}
        self.locations: dict[str, LocationData] = {}
        self.categories: dict[str, CategoryData] = {}
        self.regions: dict[str, RegionData] = {}
        self.user_options: dict[str, UserOptionData] = {}
        self.core_options: dict[str, CoreOptionData] = {}
        self.meta: MetaData = {}

    def define_item(
        self, name: str, starting_count: int | None = None, **args: Unpack[ItemArgs]
    ) -> ItemData:
        if starting_count != None:
            self.game["starting_items"] = self.game.get("starting_items") or []
            self.game["starting_items"].append(
                {"items": [name], "random": starting_count},
            )

        return self.__set_unique("Items", self.items, name, {**args, "name": name})

    def define_location(self, name: str, **args: Unpack[LocationArgs]) -> LocationData:
        return self.__set_unique(
            "Locations", self.locations, name, {**args, "name": name}
        )

    def define_category(
        self, name: str, starting_count: int | None = None, **args: Unpack[CategoryData]
    ) -> tuple[str, CategoryData]:
        if starting_count != None:
            self.game["starting_items"] = self.game.get("starting_items") or []
            self.game["starting_items"].append(
                {"item_categories": [name], "random": starting_count},
            )

        return name, self.__set_unique("Categories", self.categories, name, args)

    def define_region(
        self, name: str, **args: Unpack[RegionData]
    ) -> tuple[str, RegionData]:
        return name, self.__set_unique("Regions", self.regions, name, args)

    def define_toggle_option(
        self, name: str, **args: Unpack[ToggleOptionArgs]
    ) -> ToggleOptionSpec:
        data = ToggleOptionData(**args, type="Toggle")
        self.__set_unique("Toggle Options", self.user_options, name, data)
        return ToggleOptionSpec(name, data)

    def define_range_option(
        self, name: str, **args: Unpack[RangeOptionArgs]
    ) -> RangeOptionSpec:
        data = RangeOptionData(**args, type="Range")
        self.__set_unique("Range Options", self.user_options, name, data)
        return RangeOptionSpec(name, data)

    def define_choice_option(
        self, name: str, **args: Unpack[ChoiceOptionArgs]
    ) -> tuple[str, ChoiceOptionData]:
        data = ChoiceOptionData(**args, type="Choice")
        self.__set_unique("Choice Options", self.user_options, name, data)
        return name, data

    def define_core_option(
        self, name: str, **data: Unpack[CoreOptionData]
    ) -> tuple[str, CoreOptionData]:
        self.__set_unique("Core Options", self.core_options, name, data)
        return name, data

    @staticmethod
    def __set_unique[T](dict_name: str, dict: dict[str, T], key: str, value: T) -> T:
        if key in dict:
            raise Exception(f'"{key}" is already defined in {dict_name}')

        dict[key] = value
        return value
