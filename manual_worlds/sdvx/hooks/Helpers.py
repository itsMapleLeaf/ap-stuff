import logging
import os
from typing import Final, Optional, TYPE_CHECKING
from BaseClasses import MultiWorld, Item, Location
from worlds.AutoWorld import World


if TYPE_CHECKING:
    from ..Items import ManualItem
    from ..Locations import ManualLocation

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    if hasattr(multiworld, "generation_is_fake"):
        return None

    return None


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(
    multiworld: MultiWorld, player: int, item: dict
) -> Optional[bool]:
    if hasattr(multiworld, "generation_is_fake"):
        return None

    from ..spec import song_item_category_name
    from .State import ChartPool

    if "category" in item and song_item_category_name in item["category"]:
        return item["name"] in ChartPool.for_player(player).enabled_item_names

    return None


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(
    multiworld: MultiWorld, player: int, location: dict
) -> Optional[bool]:
    if hasattr(multiworld, "generation_is_fake"):
        return None

    from ..spec import song_location_category_name
    from .State import ChartPool

    if "category" in location and song_location_category_name in location["category"]:
        return location["name"] in ChartPool.for_player(player).enabled_location_names

    return None


class TinyLog:
    log_debug_enabled: Final = not not os.getenv("DEBUG")

    def __init__(self, player_id: int, world: World) -> None:
        from ..Data import game_table

        self.log_context = (
            f"[{game_table['game']}][Player {player_id} \"{world.player_name}\"]"
        )

        if self.log_debug_enabled:
            self.debug("Debug logging enabled")

    def debug(self, msg: str):
        if not TinyLog.log_debug_enabled:
            return
        logging.info(f"[debug] {self.log_context} {msg}")

    def warning(self, msg: str):
        logging.warning(f"[warn] {self.log_context} {msg}")

    def exception(self, msg: str):
        raise Exception(f"{self.log_context} {msg}")
