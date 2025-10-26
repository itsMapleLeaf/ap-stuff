import argparse
from dataclasses import dataclass
import glob
import os
from pathlib import Path
import shutil
from typing import Final, Generator, Iterable
from zipfile import ZipFile
import yaml

from .lib.args_override import ArgsOverride
from .lib.manual_worlds import list_project_manual_worlds
from .build import build_apworld
from .lib.paths import dist_generate_dir, dist_generate_players_dir, project_dir


def __main():
    @dataclass(init=False)
    class Args:
        game_name: str

    parser = argparse.ArgumentParser()
    parser.add_argument("game_name")

    args = parser.parse_args(None, Args())

    multiworld_config = MultiWorldConfig(
        project_dir / f"config/multiworlds/{args.game_name}.yaml"
    )

    output_dir = dist_generate_dir

    print(
        f'⚙️  Generating for "{args.game_name}"'
        f" ({multiworld_config.path.relative_to(project_dir)})"
    )

    if not multiworld_config.player_configs:
        print("⚠️ No player configs found")
        exit(1)

    player_config_world_ids = {c.game for c in multiworld_config.player_configs}
    for manual_world_project in list_project_manual_worlds():
        if manual_world_project.world_id in player_config_world_ids:
            print(f"⚙️  Building project world: {manual_world_project.world_id}")
            build_apworld(manual_world_project.src_dir)

    print(f"⚙️  Cleaning up output path")
    shutil.rmtree(output_dir)

    print(f"⚙️  Copying {len(multiworld_config.player_configs)} player configs")
    os.makedirs(dist_generate_players_dir)
    for player_config in multiworld_config.player_configs:
        shutil.copy(player_config.path, dist_generate_players_dir)

    print(f"⚙️  Running generator")

    # the generator isn't made to be invoked from a python script,
    # and the cleanest, most future-proof way to invoke it
    # is to override args so it parses them as if it were run via CLI
    #
    # gross, but better than subprocess!
    with ArgsOverride(
        # fmt: off
        "--player_files_path", dist_generate_players_dir,
        "--outputpath", output_dir,
        # fmt: on
    ):
        import Generate, Main

        (generator_args, generator_seed) = Generate.main()
        Main.main(generator_args, generator_seed)

    print(f"⚙️  Extracting files")

    generated_output_path = next(glob.iglob("AP_*.zip", root_dir=output_dir))
    with ZipFile(output_dir / generated_output_path) as generated_output_file:
        generated_output_file.extractall(output_dir)

    print(f"✅  Done")

class MultiWorldConfig:
    def __init__(self, path: Path):
        with open(path) as game_file:
            data: dict = yaml.safe_load(game_file)

        self.path: Final = path
        self.player_globs: Final[list[str]] = data["players"]
        self.player_configs: Final = list(self.__load_player_configs())

    def __load_player_configs(self) -> Generator["PlayerConfig"]:
        for player_config_file_glob in self.player_globs:
            for player_file_stem in glob.iglob(
                player_config_file_glob, root_dir="config"
            ):
                config_path = project_dir / "config" / player_file_stem
                with open(config_path, encoding="utf8") as config_file:
                    # player config files can have multiple configurations specified
                    configs: Iterable[dict] = yaml.full_load_all(config_file)
                    for config in configs:
                        yield PlayerConfig(path=config_path, data=config)


class PlayerConfig:
    def __init__(self, path: Path, data: dict):
        self.path = path
        self.game: Final[str] = data["game"]


if __name__ == "__main__":
    __main()
