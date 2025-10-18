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


def __define_world_spec() -> WorldSpec:
    spec = WorldSpec()

    songs_category = spec.define_category("Songs", starting_count=7)[0]

    def __define_songs(song_list: list[SongSpec], other_category: str | None = None):
        for song in song_list:
            for chart in song.charts:
                song_item = spec.define_item(
                    chart.item_name,
                    category=[
                        songs_category,
                        *(other_category if other_category != None else []),
                    ],
                    progression=True,
                )

                spec.define_location(
                    chart.location_name,
                    category=[
                        songs_category,
                        *(other_category if other_category != None else []),
                    ],
                    requires=Requires.item(song_item),
                )

    __define_songs(SongSpec.base_songs)

    member_songs_option = spec.define_toggle_option(
        "enable_member_songs",
        display_name="Enable Membership songs",
        description="Enable songs that require a membership subscription",
        default=False,
    )[0]
    member_songs_category = spec.define_category(
        "Member Songs",
        yaml_option=[member_songs_option],
    )[0]
    __define_songs(SongSpec.member_songs, member_songs_category)

    blaster_songs_option = spec.define_toggle_option(
        "enable_blaster_gate_songs",
        display_name="Enable BLASTER GATE songs",
        description="Enable songs unlocked through BLASTER GATE",
        default=False,
    )[0]
    blaster_songs_category = spec.define_category(
        "BLASTER GATE",
        yaml_option=[blaster_songs_option],
    )[0]
    __define_songs(SongSpec.blaster_songs, blaster_songs_category)

    spec.define_location(
        "Boss Song",
        category="Boss Song",
        requires=Requires.category("Songs", "70%"),
        victory=True,
    )

    return spec


spec = __define_world_spec()
