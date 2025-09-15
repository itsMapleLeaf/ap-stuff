import glob
from shutil import copy
from sys import argv
import yaml
from ._paths import project_dir


def list_player_file_paths(game_name: str):
    with open(project_dir / f"games/{game_name}.yaml") as game_file:
        game_data = yaml.safe_load(game_file)

    for player_spec in game_data["players"]:
        for player_file_stem in glob.iglob(player_spec, root_dir="players"):
            yield project_dir / "players" / player_file_stem


def __main() -> None:
    game_name_arg = argv[1]
    for player_file_path in list_player_file_paths(game_name_arg):
        print(copy(player_file_path, project_dir / "dist/generate/players"))


if __name__ == "__main__":
    __main()
