from dataclasses import dataclass


@dataclass
class Song:
    id: str
    title: str
    artist: str
    groups: list[str]
    charts: dict[str, int]

    @property
    def id_category_name(self) -> str:
        return f"Song ID {self.id}"
