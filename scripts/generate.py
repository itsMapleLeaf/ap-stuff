import argparse
from dataclasses import dataclass
import glob
import logging
import os
from pathlib import Path
import shutil
import subprocess
from typing import Generator, TypedDict
import yaml

from .build import build_all_project_manual_worlds
from .paths import (
    dist_generate_dir,
    dist_generate_players_dir,
    project_dir,
)


def __main():
    @dataclass(init=False)
    class Args:
        game_name: str

    parser = argparse.ArgumentParser()
    parser.add_argument("game_name")

    args = parser.parse_args(None, Args())
    multiworld_config_path = project_dir / f"config/multiworlds/{args.game_name}.yaml"

    build_all_project_manual_worlds()

    print(
        f'⚙️  Generating for "{args.game_name}"'
        f" ({multiworld_config_path.relative_to(project_dir)})"
    )

    player_config_paths = list(__list_player_file_paths(multiworld_config_path))
    if not player_config_paths:
        logging.error("⚠️ No player configs found")
        exit(1)

    print(f"⚙️  Removing generate dir")
    shutil.rmtree(dist_generate_dir)

    print(f"⚙️  Copying {len(player_config_paths)} player configs")
    os.makedirs(dist_generate_players_dir)
    for player_config_path in player_config_paths:
        shutil.copy(player_config_path, dist_generate_players_dir)

    print(f"⚙️  Running generator")
    subprocess.run(
        [
            *["uv", "run", "-m", "archipelago.Generate"],
            *["--player_files_path", dist_generate_players_dir],
            *["--outputpath", dist_generate_dir],
        ],
        cwd=project_dir,
    )

    print(f"✅  Done")


def __list_player_file_paths(multiworld_config_path: Path) -> Generator[Path]:
    class GameData(TypedDict):
        players: list[str]

    with open(multiworld_config_path) as game_file:
        game_data: GameData = yaml.safe_load(game_file)

    for player_config_file_glob in game_data["players"]:
        for player_file_stem in glob.iglob(player_config_file_glob, root_dir="config"):
            yield project_dir / "config" / player_file_stem


if __name__ == "__main__":
    __main()
