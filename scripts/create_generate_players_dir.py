import glob
from pathlib import Path
from shutil import copy
from sys import argv
from typing import Generator, TypedDict
import yaml
from .paths import project_dir


def list_player_file_paths(game_name: str) -> Generator[Path]:
    class GameData(TypedDict):
        players: list[str]

    with open(project_dir / f"config/multiworlds/{game_name}.yaml") as game_file:
        game_data: GameData = yaml.safe_load(game_file)

    for player_spec in game_data["players"]:
        for player_file_stem in glob.iglob(player_spec, root_dir="config"):
            yield project_dir / "config" / player_file_stem


def __main() -> None:
    game_name_arg = argv[1]
    match list(list_player_file_paths(game_name_arg)):
        case []:
            print(f'No player files found for game "{game_name_arg}"')
            exit(1)
        case paths:
            for player_file_path in paths:
                print(copy(player_file_path, project_dir / "dist/generate/players"))


if __name__ == "__main__":
    __main()
