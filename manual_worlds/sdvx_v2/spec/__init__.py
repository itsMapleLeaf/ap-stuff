from dataclasses import dataclass, field
import hashlib
import re
from typing import ClassVar, Literal, NotRequired, TypedDict

from .requires import Requires
from ..Helpers import load_data_file
from .world import WorldSpec


@dataclass
class SongSpec:
    title: str
    artist: str
    charts: list["Chart"]
    pack: str | None = None

    type Difficulty = Literal["nov", "adv", "exh", "mxm"]
    diffs: ClassVar[list[Difficulty]] = ["nov", "adv", "exh", "mxm"]

    songs_data: ClassVar[dict]
    base_songs: ClassVar[list["SongSpec"]]
    member_songs: ClassVar[list["SongSpec"]]
    blaster_songs: ClassVar[list["SongSpec"]]
    pack_songs: ClassVar[list["SongSpec"]]
    packs: ClassVar[set[str]]

    class Data(TypedDict):
        title: str
        artist: str
        bpm: str
        nov: str
        adv: str
        exh: str
        mxm: str
        pack: NotRequired[str]

    @dataclass
    class Chart:
        diff: str
        level: int
        song: "SongSpec"

        @property
        def summary(self):
            return f"{self.diff.upper()} {self.level}"

        @property
        def item_name(self):
            return f"{self.song.safe_title} - {self.summary}"

        @property
        def location_name(self):
            return f"{self.song.title} - {self.summary}"

    @staticmethod
    def from_data(data: Data) -> "SongSpec":
        spec = SongSpec(
            title=data["title"],
            artist=data["artist"],
            pack=data.get("pack", None),
            charts=[],
        )

        for diff in SongSpec.diffs:
            if data.get(diff, "").isdigit():
                spec.charts.append(
                    SongSpec.Chart(diff=diff, level=int(data[diff]), song=spec)
                )

        return spec

    @property
    def safe_title(self):
        return re.sub(r"\s*[:|]\s*", " ", self.title)


SongSpec.songs_data = load_data_file("songs.json")

SongSpec.base_songs = [SongSpec.from_data(data) for data in SongSpec.songs_data["base"]]
SongSpec.member_songs = [
    SongSpec.from_data(data) for data in SongSpec.songs_data["member"]
]
SongSpec.blaster_songs = [
    SongSpec.from_data(data) for data in SongSpec.songs_data["blaster"]
]
SongSpec.pack_songs = [SongSpec.from_data(data) for data in SongSpec.songs_data["pack"]]

SongSpec.packs = {song.pack for song in SongSpec.pack_songs if song.pack != None}


def __define_world_spec() -> WorldSpec:
    spec = WorldSpec()

    songs_category = spec.define_category("Songs", starting_count=7)[0]

    for song in SongSpec.base_songs:
        for chart in song.charts:
            song_item = spec.define_item(
                chart.item_name,
                category=[songs_category, "Base Songs"],
                progression=True,
            )["name"]

            spec.define_location(
                chart.location_name,
                category=[songs_category, "Base Songs"],
                requires=Requires.item(song_item),
            )

    spec.define_location(
        "Boss Song",
        category="Boss Song",
        requires=Requires.category("Songs", "70%"),
        victory=True,
    )

    return spec


spec = __define_world_spec()
