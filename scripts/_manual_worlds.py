from dataclasses import dataclass
import os
from pathlib import Path
from typing import Generator
from ._paths import worlds_dir


@dataclass
class ManualWorldInfo:
    name: str

    @property
    def root_dir(self) -> Path:
        return worlds_dir / self.name

    @property
    def src_dir(self) -> Path:
        return self.root_dir


def list_project_manual_worlds() -> Generator[ManualWorldInfo]:
    for world_name in os.listdir(worlds_dir):
        yield ManualWorldInfo(name=world_name)
