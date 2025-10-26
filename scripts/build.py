from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory

from .inspect import inspect_manual_world
from .paths import user_archipelago_worlds_dir


def build_apworld(
    src_dir: Path, output_dir: str | Path = user_archipelago_worlds_dir
) -> Path:
    output_dir = Path(output_dir)

    world_data = inspect_manual_world(src_dir)

    with TemporaryDirectory() as temp_archive_root:
        apworld_base_name = (
            f"manual_{world_data.game_table.game}_{world_data.game_table.creator}"
        )

        shutil.copytree(
            src=src_dir,
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


def build_all_project_manual_worlds():
    from .manual_worlds import list_project_manual_worlds

    available_worlds = [*list_project_manual_worlds()]

    world_args = set(sys.argv[1:])
    worlds_to_build = [
        world for world in available_worlds if world.name in world_args
    ] or available_worlds

    for world in worlds_to_build:
        print(f"Building {world.name}...")
        final_destination_fox_only_no_items = build_apworld(
            world.src_dir, user_archipelago_worlds_dir
        )
        print(f"Built at {final_destination_fox_only_no_items}")


if __name__ == "__main__":
    build_all_project_manual_worlds()
