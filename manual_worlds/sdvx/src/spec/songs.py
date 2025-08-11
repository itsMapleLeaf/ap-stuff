from dataclasses import dataclass


@dataclass
class Song:
    id: str
    title: str
    artist: str
    groups: list[str]
    charts: dict[str, int]
