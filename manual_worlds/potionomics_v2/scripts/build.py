import importlib.util
from os import environ
from pathlib import Path
import random
import shutil
import sys
from tempfile import TemporaryDirectory

src_dir = Path(__file__).parent.parent / "src"

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

game: str = data_module.game_table["game"]
creator: str = data_module.game_table["creator"]

with TemporaryDirectory() as temp_archive_root:
    apworld_base_name = f"manual_{game}_{creator}"

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

apworld_output_dir = Path(
    environ.get("OUTPUT_DIR", "C:/ProgramData/Archipelago/custom_worlds")
)

final_destination_fox_only_no_items = shutil.move(
    src=apworld_zip,
    dst=apworld_output_dir / f"{apworld_base_name}.apworld",
)

print(f"Built at {final_destination_fox_only_no_items}")
