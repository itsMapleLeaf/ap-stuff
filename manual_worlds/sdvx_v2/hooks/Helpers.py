from typing import Optional, TYPE_CHECKING
from BaseClasses import MultiWorld, Item, Location

if TYPE_CHECKING:
    from ..Items import ManualItem
    from ..Locations import ManualLocation

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    return None


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(
    multiworld: MultiWorld, player: int, item: dict
) -> Optional[bool]:
    from .State import player_chart_pools

    if "Songs" in item["category"]:
        return any(
            chart.item_name == item["name"] for chart in player_chart_pools[player]
        )

    return None


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(
    multiworld: MultiWorld, player: int, location: dict
) -> Optional[bool]:
    from .State import player_chart_pools

    if "Songs" in location["category"]:
        return any(
            chart.location_name == location["name"]
            for chart in player_chart_pools[player]
        )

    return None
