import os
import shutil
import sys
from showinfm.showinfm import show_in_file_manager
import yaml

from ._manual_worlds import list_project_manual_worlds
from .build import make_apworld
from ._paths import project_dir


def __main():
    game_arg = sys.argv[1]

    game_dir = project_dir / "games" / game_arg
    output_dir = project_dir / "dist/export" / game_arg

    combined_player_config_file_name = "Maple.yaml"

    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir)

    for world in list_project_manual_worlds():
        make_apworld(world, output_dir=output_dir)

    player_configs = []
    for player_config_file_name in os.listdir(game_dir):
        if not player_config_file_name.endswith(".yaml"):
            continue

        with open(
            game_dir / player_config_file_name, encoding="utf8"
        ) as player_config_file:
            player_configs.append(yaml.safe_load(player_config_file))

    combined_player_config_path = output_dir / combined_player_config_file_name

    with open(
        combined_player_config_path, "w", encoding="utf8"
    ) as combined_player_config_file:
        yaml.dump_all(
            player_configs,
            combined_player_config_file,
            sort_keys=False,
            allow_unicode=True,
        )

    show_in_file_manager(str(output_dir))


if __name__ == "__main__":
    __main()
