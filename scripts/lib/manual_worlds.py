from dataclasses import dataclass
import os
from pathlib import Path
from typing import Generator

from ..inspect import ManualWorldData, inspect_manual_world
from ..build import build_apworld
from .paths import project_worlds_dir


@dataclass
class ManualWorldProject:
    name: str

    @property
    def root_dir(self) -> Path:
        return project_worlds_dir / self.name

    @property
    def src_dir(self) -> Path:
        return self.root_dir

    def inspect(self) -> ManualWorldData:
        return inspect_manual_world(self.src_dir)

    @property
    def world_id(self) -> str:
        game_info = self.inspect().game_table
        return f"Manual_{game_info.game}_{game_info.creator}"

    def build(self):
        return build_apworld(self.src_dir)


def list_project_manual_worlds() -> Generator[ManualWorldProject]:
    for world_name in os.listdir(project_worlds_dir):
        yield ManualWorldProject(name=world_name)
