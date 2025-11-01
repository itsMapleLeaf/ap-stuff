import glob
from pathlib import Path
from typing import Final, Generator, Iterable
import yaml

from .paths import project_dir


class MultiWorldConfig:
    @staticmethod
    def named(name: str):
        return MultiWorldConfig(project_dir / f"config/multiworlds/{name}.yaml")

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
        self.data = data
        self.game: Final[str] = data["game"]
