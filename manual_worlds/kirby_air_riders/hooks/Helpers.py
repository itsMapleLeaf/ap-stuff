from typing import Optional, Any, cast
from BaseClasses import MultiWorld


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(
    multiworld: MultiWorld, player: int, category_name: str
) -> Optional[bool]:
    if hasattr(multiworld, "generation_is_fake"):
        return None

    return None


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(
    multiworld: MultiWorld, player: int, item: dict[str, Any]
) -> Optional[bool]:
    if hasattr(multiworld, "generation_is_fake"):
        return None

    return None


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(
    multiworld: MultiWorld, player: int, location: dict[str, Any]
) -> Optional[bool]:
    if hasattr(multiworld, "generation_is_fake"):
        return None

    from ..Helpers import get_option_value

    goal_stage = cast(int, get_option_value(multiworld, player, "goal_stage"))
    disabled_stages = {
        f"Road Trip - Complete Stage {i} (Goal)" for i in range(1, goal_stage)
    }

    if location["name"] in disabled_stages:
        return False

    return None
