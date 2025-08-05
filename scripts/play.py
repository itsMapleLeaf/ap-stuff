import os
from pathlib import Path
import shutil
import yaml

from .build import make_apworld


combined_player_config_file_name = "Maple.yaml"

project_dir = Path(__file__).parent.parent
worlds_dir = project_dir / "worlds"
dist_dir = project_dir / "dist"
players_dir = project_dir / "players"


shutil.rmtree(dist_dir)
os.makedirs(dist_dir)

for world_name in os.listdir(worlds_dir):
    world_dir = worlds_dir / world_name
    make_apworld(world_dir=world_dir, output_dir=dist_dir)


player_configs = []
for player_config_file_name in os.listdir(players_dir):
    with open(
        players_dir / player_config_file_name, encoding="utf8"
    ) as player_config_file:
        player_configs.append(yaml.safe_load(player_config_file))

combined_player_config_path = dist_dir / combined_player_config_file_name

with open(
    combined_player_config_path, "w", encoding="utf8"
) as combined_player_config_file:
    yaml.dump_all(
        player_configs, combined_player_config_file, sort_keys=False, allow_unicode=True
    )

print(f"Wrote combined player config to {combined_player_config_path}")
