import glob
from pathlib import Path
from shutil import copy
from sys import argv
from typing import TypedDict

import yaml


def __main() -> None:
    game_name_arg = argv[1]

    class GameData(TypedDict):
        players: list[str]

    with open(Path("games") / f"{game_name_arg}.yaml") as game_file:
        game_data: GameData = yaml.safe_load(game_file)

    for player_spec in game_data["players"]:
        for player_file_name in glob.iglob(
            player_spec,
            root_dir="players",
        ):
            print(
                copy(Path("players") / player_file_name, Path("dist/generate/players"))
            )


__main()
