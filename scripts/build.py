from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory

from ._manual_worlds import ManualWorldInfo, list_project_manual_worlds
from .inspect import inspect_manual_world
from ._paths import user_archipelago_worlds_dir


def make_apworld(world: ManualWorldInfo, output_dir: str | Path) -> Path:
    output_dir = Path(output_dir)

    world_data = inspect_manual_world(world)

    with TemporaryDirectory() as temp_archive_root:
        apworld_base_name = (
            f"manual_{world_data.game_table.game}_{world_data.game_table.creator}"
        )

        shutil.copytree(
            src=world.src_dir,
            dst=Path(temp_archive_root) / apworld_base_name,
        )

        apworld_zip = shutil.make_archive(
            base_name=apworld_base_name,
            format="zip",
            root_dir=temp_archive_root,
            base_dir=".",
            verbose=True,
        )

    return Path(
        shutil.move(
            src=apworld_zip,
            dst=output_dir / f"{apworld_base_name}.apworld",
        )
    )


def __main():
    available_worlds = [*list_project_manual_worlds()]

    world_args = set(sys.argv[1:])
    worlds_to_build = [
        world for world in available_worlds if world.name in world_args
    ] or available_worlds

    for world in worlds_to_build:
        print(f"Building {world.name}...")
        final_destination_fox_only_no_items = make_apworld(
            world, user_archipelago_worlds_dir
        )
        print(f"Built at {final_destination_fox_only_no_items}")


if __name__ == "__main__":
    __main()
