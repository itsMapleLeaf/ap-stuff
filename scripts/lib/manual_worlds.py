from dataclasses import dataclass
import warnings
from dataclasses_json import DataClassJsonMixin
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator, Literal, Optional
import shutil
import importlib.util
import sys

from .paths import project_worlds_dir, user_archipelago_worlds_dir


class ManualWorldProject:
    def __init__(self, src: Path, name: str | None = None):
        self.path = src
        self.name = name or src.stem

    @property
    @warnings.deprecated("Use 'path' instead of 'src")
    def src(self) -> Path:
        return self.path

    @staticmethod
    def local(name: str):
        return ManualWorldProject(
            name=name,
            src=project_worlds_dir / name,
        )

    @property
    def world_id(self) -> str:
        game_info = self.inspect().game_table
        return f"Manual_{game_info.game}_{game_info.creator}"

    def build(self, output_dir: Path = user_archipelago_worlds_dir):
        world_data = self.inspect()

        with TemporaryDirectory() as temp_archive_root:
            apworld_base_name = (
                f"manual_{world_data.game_table.game}_{world_data.game_table.creator}"
            )

            shutil.copytree(
                src=self.src,
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

    def inspect(self) -> "ManualWorldData":
        data_module = self.load_module("Data")

        def resolve_list(key: str):
            value = getattr(data_module, key, None)
            return value if isinstance(value, list) else []

        def resolve_dict(key: str):
            value = getattr(data_module, key, None)
            return value if isinstance(value, dict) else {}

        return ManualWorldData(
            game_table=ManualGameData.from_dict(resolve_dict("game_table")),
            item_table=resolve_list("item_table"),
            location_table=resolve_list("location_table"),
            category_table=resolve_dict("category_table"),
            option_table=resolve_dict("option_table"),
            region_table=resolve_dict("region_table"),
            meta_table=resolve_dict("meta_table"),
        )

    def load_module(self, module_name: Literal["Data"] | str):
        module_file_path = self.src / f"{module_name}.py"

        # key by the manual project name,
        # so it doesn't cache other manual project modules by the same name
        module_key = f"manual_data_{self.name}"

        module_spec = importlib.util.spec_from_file_location(
            name=module_key,
            location=module_file_path,
            submodule_search_locations=[str(self.src)],
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


def find_local_manual_world_projects() -> Generator[ManualWorldProject]:
    ignored = {".vscode"}
    for entry in os.scandir(project_worlds_dir):
        if entry.is_dir() and entry.name not in ignored:
            yield ManualWorldProject.local(entry.name)


@dataclass
class ManualWorldData:
    game_table: "ManualGameData"
    item_table: list
    location_table: list
    category_table: dict
    option_table: dict
    region_table: dict
    meta_table: dict

    def __post_init__(self) -> None:
        self.item_count = (
            sum(self.__item_count_of(item) for item in self.item_table)
            if self.item_table
            else 0
        )
        self.location_count = len(self.location_table) if self.location_table else 0

        self.progression_item_count = 0
        self.useful_item_count = 0
        self.filler_item_count = 0

        for item in self.item_table or []:
            match item:
                case {"classification_count": {**counts}}:
                    for key, count in counts.items():
                        if "progression" in key:
                            self.progression_item_count += count
                        elif "useful" in key:
                            self.useful_item_count += count
                        elif "filler" in key:
                            self.filler_item_count += count

                case {
                    "progression": True,
                    "count": count,
                } | {
                    "progression_skip_balancing": True,
                    "count": count,
                }:
                    self.progression_item_count += count

                case {"progression": True} | {"progression_skip_balancing": True}:
                    self.progression_item_count += 1

                case {"useful": True, "count": count}:
                    self.useful_item_count += count

                case {"useful": True}:
                    self.useful_item_count += 1

                case {"filler": True, "count": count}:
                    self.filler_item_count += count

                case {"filler": True}:
                    self.filler_item_count += 1

                case {"count": count}:
                    self.filler_item_count += count

                case _:
                    self.filler_item_count += 1

    @staticmethod
    def __item_count_of(item: dict) -> int:
        return (
            "classification_count" in item
            and sum(item["classification_count"].values())
            or item.get("count", 1)
        )


@dataclass
class ManualGameData(DataClassJsonMixin):
    game: str
    creator: Optional[str] = None
    player: Optional[str] = None
