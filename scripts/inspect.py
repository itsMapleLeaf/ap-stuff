from dataclasses import dataclass
import importlib.util
from pathlib import Path
import random
import sys

from dataclasses_json import DataClassJsonMixin


@dataclass
class GameData(DataClassJsonMixin):
    game: str
    creator: str


@dataclass
class WorldData:
    game_table: GameData


def inspect_manual_world(world_dir: str | Path) -> WorldData:
    src_dir = Path(world_dir) / "src"

    # create a random module name to avoid caching,
    # making sure we're always loading a fresh module
    data_module_name = f"manual_data_{random.randbytes(16).hex()}"

    data_module_spec = importlib.util.spec_from_file_location(
        name=data_module_name,
        location=src_dir / "Data.py",
        submodule_search_locations=[str(src_dir)],
    )

    if not data_module_spec or not data_module_spec.loader:
        raise Exception(f"Failed to create module spec for {src_dir / "Data.py"}")

    data_module = importlib.util.module_from_spec(data_module_spec)
    sys.modules[data_module_name] = data_module

    original_sys_path = sys.path.copy()
    try:
        # sys.path.append(self.archipelago_repo_dir.as_posix())
        data_module_spec.loader.exec_module(data_module)
    finally:
        sys.path = original_sys_path

    return WorldData(
        game_table=GameData.from_dict(data_module.game_table),
    )
