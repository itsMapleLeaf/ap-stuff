from dataclasses import dataclass
import dataclasses
import importlib.util
import json
import os
from pathlib import Path
import random
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import argparse

from .lib.manual_worlds import ManualWorldProject


def load_manual_world_module(src_dir: Path, module_name: str) -> object:
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


def __main() -> None:
    from .lib.paths import project_worlds_dir, user_archipelago_worlds_dir

    @dataclass
    class Args:
        world: str = ""
        summary: bool = False

    parser = argparse.ArgumentParser(description="Inspect AP Manual world data")
    parser.add_argument("world", help="World name or path to inspect")
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Display a summary instead of full JSON output",
    )

    args = Args()
    parser.parse_args(namespace=args)

    potential_world_src_paths = [
        project_worlds_dir / args.world,
        project_worlds_dir / args.world / "src",
        user_archipelago_worlds_dir / f"{args.world}.apworld",
        user_archipelago_worlds_dir / args.world,
        Path.cwd() / args.world,
    ]

    world_src = next(
        (path for path in potential_world_src_paths if path.exists()), None
    )

    if not world_src:
        print(f'Failed to find world "{args.world}"')
        print("Searched paths:")
        for path in potential_world_src_paths:
            print("-", path.relative_to(Path.cwd()))
        exit(1)

    world_data = None

    if world_src.match("*.apworld"):
        with TemporaryDirectory() as temp_world_dir:
            with ZipFile(world_src) as world_zip:
                world_zip.extractall(temp_world_dir)
            world_src = Path(temp_world_dir) / os.listdir(temp_world_dir)[0]
            world_data = ManualWorldProject(src=world_src).inspect()
    else:
        world_data = ManualWorldProject(src=world_src).inspect()

    if args.summary:
        print(f"Game: {world_data.game_table.game}")
        print(f"Creator: {world_data.game_table.creator}")
        print(f"Player: {world_data.game_table.player}")
        print(f"Location Count: {world_data.location_count}")
        print(f"Item Count: {world_data.item_count}")
        print(f"Progression Item Count: {world_data.progression_item_count}")
        print(f"Useful Item Count: {world_data.useful_item_count}")
        print(f"Filler Item Count: {world_data.filler_item_count}")
    else:
        json.dump(dataclasses.asdict(world_data), fp=sys.stdout, indent=4)


if __name__ == "__main__":
    __main()
