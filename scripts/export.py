from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import yaml

from .inspect import inspect_manual_world
from .build import make_apworld


@dataclass
class PlayerConfig:
    player_name: str
    description: str


default_player_name = "Maple"

player_configs: dict[str, PlayerConfig] = {
    "distance": PlayerConfig(
        player_name="MapleDistance",
        description="𝘀 𝘂 𝗿 𝘃 𝗶 𝘃 𝗲   𝘁 𝗵 𝗲   𝗱 𝗶 𝘀 𝘁 𝗮 𝗻 𝗰 𝗲",
    ),
    "sdvx": PlayerConfig(
        player_name="MapleVoltex",
        description="funny bang woosh rhythm game",
    ),
}

project_dir = Path(__file__).parent.parent
worlds_dir = project_dir / "worlds"
dist_dir = project_dir / "dist"

game_configs = []

shutil.rmtree(dist_dir)
os.makedirs(dist_dir)

for world_name in os.listdir(worlds_dir):
    world_dir = worlds_dir / world_name
    make_apworld(world_dir=world_dir, output_dir=dist_dir)
    world_data = inspect_manual_world(world_dir)

    game_identifier = (
        f"Manual_{world_data.game_table.game}_{world_data.game_table.creator}"
    )

    player_config = player_configs.get(
        world_name,
        PlayerConfig(
            player_name=f"{default_player_name}{world_data.game_table.game}",
            description=f"a manual for {world_data.game_table.game}",
        ),
    )

    game_configs.append(
        {
            "name": player_config.player_name,
            "description": player_config.description,
            "game": game_identifier,
            "requires": {"version": "0.6.2"},
            game_identifier: {
                # TODO: un-hardcoded world-specific options,
                # probably requires loading from Options.py
                "progression_balancing": {
                    "random": 0,
                    "random-low": 0,
                    "random-high": 0,
                    "disabled": 0,
                    "normal": 50,
                    "extreme": 0,
                },
                "accessibility": {"full": 50, "minimal": 0},
                "plando_items": [],
                "local_items": [],
                "non_local_items": [],
                "start_inventory": {},
                "start_inventory_from_pool": {},
                "start_hints": [],
                "start_location_hints": [],
                "exclude_locations": [],
                "priority_locations": [],
                "item_links": [],
            },
        }
    )

config_file_path = dist_dir / f"{default_player_name}.yaml"

with open(config_file_path, "w", encoding="utf8") as config_file:
    yaml.dump_all(game_configs, config_file, sort_keys=False, allow_unicode=True)

print(f"Wrote stitched config to {config_file_path}")
