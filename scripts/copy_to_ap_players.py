"""
This script accepts a multiworld (from config/multiworlds/[name].yaml), then copies them into the `archipelago/Players` folder, so they can be used with UT.

This script should be run alongside other flows (such as `generate` and `export`) to ensure UT works with the relevant worlds.
"""

import os
from pathlib import Path
import shutil
import sys
from showinfm.showinfm import show_in_file_manager
import yaml

from .lib.multiworld import MultiWorldConfig
from .lib.paths import (
    project_dir,
    user_archipelago_players_dir,
    user_archipelago_worlds_dir,
)


def __main():
    multiworld_arg = sys.argv[1]
    multiworld_config = MultiWorldConfig.named(multiworld_arg)

    for entry in os.listdir(user_archipelago_players_dir):
        entry = user_archipelago_players_dir / entry
        if entry.suffix == ".yaml":
            print(f"Removing {entry.relative_to(project_dir)}")
            entry.unlink()

    for player_config in multiworld_config.player_configs:
        link_path = Path(user_archipelago_players_dir / player_config.path.name)
        print(
            f"Linking {link_path.relative_to(project_dir)} to {player_config.path.relative_to(project_dir)}"
        )
        link_path.symlink_to(player_config.path)


if __name__ == "__main__":
    __main()
