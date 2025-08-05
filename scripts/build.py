from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

from .inspect import inspect_manual_world


def make_apworld(world_dir: str | Path, output_dir: str | Path) -> None:
    world_dir = Path(world_dir)
    output_dir = Path(output_dir)
    src_dir = Path(world_dir) / "src"

    world_data = inspect_manual_world(world_dir)

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

    final_destination_fox_only_no_items = shutil.move(
        src=apworld_zip,
        dst=output_dir / f"{apworld_base_name}.apworld",
    )

    print(f"Built at {final_destination_fox_only_no_items}")


if __name__ == "__main__":
    make_apworld(
        Path(__file__).parent.parent, "C:/ProgramData/Archipelago/custom_worlds"
    )
