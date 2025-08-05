from dataclasses import dataclass
import importlib.util
from pathlib import Path
import random
import sys
from typing import Any
from dataclasses_json import DataClassJsonMixin


@dataclass
class GameData(DataClassJsonMixin):
    game: str
    creator: str


@dataclass
class WorldData:
    game_table: GameData


def inspect_manual_world(world_dir: str | Path) -> WorldData:
    data_module: Any = load_manual_world_module(world_dir, "Data")
    return WorldData(
        game_table=GameData.from_dict(data_module.game_table),
    )


def load_manual_world_module(world_dir: str | Path, module_name: str) -> object:
    src_dir = Path(world_dir) / "src"
    module_file_path = src_dir / f"{module_name}.py"

    # create a random module name to avoid caching,
    # making sure we're always loading a fresh module
    module_key = f"manual_data_{random.randbytes(16).hex()}"

    module_spec = importlib.util.spec_from_file_location(
        name=module_key,
        location=module_file_path,
        submodule_search_locations=[str(src_dir)],
    )

    if not module_spec or not module_spec.loader:
        raise Exception(f"Failed to create module spec for {module_file_path}")

    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_key] = module

    original_sys_path = sys.path.copy()
    try:
        # sys.path.append(self.archipelago_repo_dir.as_posix())
        module_spec.loader.exec_module(module)
    finally:
        sys.path = original_sys_path

    return module
