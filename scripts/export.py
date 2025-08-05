import os
import shutil
import yaml

from ._manual_worlds import list_project_manual_worlds
from .build import make_apworld
from ._paths import players_dir, project_dir

dist_dir = project_dir / "dist"

combined_player_config_file_name = "Maple.yaml"


shutil.rmtree(dist_dir)
os.makedirs(dist_dir)

for world in list_project_manual_worlds():
    make_apworld(world, output_dir=dist_dir)


player_configs = []
for player_config_file_name in os.listdir(players_dir):
    if not player_config_file_name.endswith(".yaml"):
        continue

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
