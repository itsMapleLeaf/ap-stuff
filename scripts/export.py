import os
import shutil
import sys
from showinfm.showinfm import show_in_file_manager
import yaml

from .create_generate_players_dir import list_player_file_paths

from .lib.paths import project_dir, user_archipelago_worlds_dir


def __main():
    game_arg = sys.argv[1]
    output_dir = project_dir / "dist/export" / game_arg
    combined_player_config_file_name = "Maple.yaml"

    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir)

    player_configs = []
    for player_config_path in list_player_file_paths(game_arg):
        with open(player_config_path, encoding="utf8") as player_config_file:
            player_configs.append(yaml.safe_load(player_config_file))

    combined_config_path = output_dir / combined_player_config_file_name

    with open(combined_config_path, "w", encoding="utf8") as combined_config_file:
        yaml.dump_all(
            player_configs,
            combined_config_file,
            sort_keys=False,
            allow_unicode=True,
        )

    included_worlds = {
        user_archipelago_worlds_dir
        / f"{str(config['game']).replace('Manual','manual',1)}.apworld"
        for config in player_configs
        if "Manual" in str(config["game"])
    }

    for world_path in included_worlds:
        shutil.copy(world_path, output_dir)

    show_in_file_manager(str(output_dir))


if __name__ == "__main__":
    __main()
