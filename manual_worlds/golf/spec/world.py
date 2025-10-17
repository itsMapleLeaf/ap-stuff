from typing import Unpack

from .types import (
    CategoryData,
    ChoiceOptionArgs,
    ChoiceOptionData,
    CoreOptionData,
    GameData,
    ItemArgs,
    ItemData,
    LocationArgs,
    LocationData,
    MetaData,
    RangeOptionArgs,
    RangeOptionData,
    RegionData,
    ToggleOptionArgs,
    ToggleOptionData,
    UserOptionData,
)


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
            self.game.setdefault("starting_items", []).append(
                {"items": [name], "random": starting_count},
            )

        return self.__set_unique("Items", self.items, name, {**args, "name": name})

    def define_location(self, name: str, **args: Unpack[LocationArgs]) -> LocationData:
        return self.__set_unique(
            "Locations", self.locations, name, {**args, "name": name}
        )

    def define_category(
        self, name: str, **args: Unpack[CategoryData]
    ) -> tuple[str, CategoryData]:
        return name, self.__set_unique("Categories", self.categories, name, args)

    def define_region(
        self, name: str, **args: Unpack[RegionData]
    ) -> tuple[str, RegionData]:
        return name, self.__set_unique("Regions", self.regions, name, args)

    def define_toggle_option(
        self, name: str, **args: Unpack[ToggleOptionArgs]
    ) -> tuple[str, ToggleOptionData]:
        data = ToggleOptionData(**args, type="Toggle")
        self.__set_unique("Toggle Options", self.user_options, name, data)
        return name, data

    def define_range_option(
        self, name: str, **args: Unpack[RangeOptionArgs]
    ) -> tuple[str, RangeOptionData]:
        data = RangeOptionData(**args, type="Range")
        self.__set_unique("Range Options", self.user_options, name, data)
        return name, data

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
