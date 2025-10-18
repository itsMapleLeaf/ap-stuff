from dataclasses import dataclass, field
import dataclasses
import hashlib
from math import floor
import re
from typing import ClassVar, Iterable, Literal, NotRequired, TypedDict
from unicodedata import category

from .requires import Requires
from ..Helpers import load_data_file
from .world import WorldSpec


class SongData(TypedDict):
    title: str
    artist: str
    bpm: str
    nov: str
    adv: str
    exh: str
    mxm: str
    pack: NotRequired[str]


@dataclass
class SongSpec:
    title: str
    artist: str
    charts: list["Chart"]

    type Difficulty = Literal["nov", "adv", "exh", "mxm"]
    diffs: ClassVar[list[Difficulty]] = ["nov", "adv", "exh", "mxm"]

    songs_data: ClassVar[dict]
    base_songs: ClassVar[list["SongSpec"]]
    member_songs: ClassVar[list["SongSpec"]]
    blaster_songs: ClassVar[list["SongSpec"]]
    pack_songs: ClassVar[list["PackSongSpec"]]
    packs: ClassVar[set[str]]

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
        def location_names(self):
            return [
                f"{self.song.title} - {self.summary} - Track Clear",
                f"{self.song.title} - {self.summary} - Gate Clear",
            ]

    @staticmethod
    def from_data(data: SongData) -> "SongSpec":
        spec = SongSpec(
            title=data["title"],
            artist=data["artist"],
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


@dataclass
class PackSongSpec(SongSpec):
    pack: str

    all_song_packs: ClassVar = [
        "楽曲パック vol.1",
        "楽曲パック vol.2",
        "楽曲パック vol.3",
        "楽曲パック vol.4",
        "楽曲パック vol.5",
        "楽曲パック vol.6",
        "楽曲パック vol.7",
        "楽曲パック vol.8",
        "楽曲パック vol.9",
        "楽曲パック vol.10",
        "楽曲パック vol.11",
        "楽曲パック vol.12",
        "楽曲パック vol.13",
        "楽曲パック vol.14",
        "楽曲パック vol.15",
        "楽曲パック vol.16",
        "楽曲パック vol.17",
        "楽曲パック vol.18",
        "楽曲パック vol.19",
        "楽曲パック vol.20",
        "楽曲パック vol.21",
        "楽曲パック vol.22",
        "楽曲パック vol.23",
        "楽曲パック vol.24",
        "楽曲パック vol.25",
        "10周年記念 楽曲パック",
        "BEMANI セレクション 楽曲パック vol.1",
        "BEMANI セレクション 楽曲パック vol.2",
        "BEMANI セレクション 楽曲パック vol.3",
        "MÚSECAセレクション 楽曲パック vol.1",
        "MÚSECAセレクション 楽曲パック vol.2",
        "REFLEC BEAT セレクション 楽曲パック vol.1",
        "beatmania IIDX セレクション 楽曲パック vol.1",
        "jubeat セレクション 楽曲パック vol.1",
        "ここなつセレクション 楽曲パック",
        "スタートアップセレクション 楽曲パック vol.1",
        "東方Projectセレクション 楽曲パック",
    ]

    @staticmethod
    def from_data(data: SongData) -> "PackSongSpec":
        base_spec = SongSpec.from_data(data)
        return PackSongSpec(
            title=base_spec.title,
            artist=base_spec.artist,
            charts=base_spec.charts,
            pack=data.get("pack", ""),
        )


SongSpec.songs_data = load_data_file("songs.json")

SongSpec.base_songs = [SongSpec.from_data(data) for data in SongSpec.songs_data["base"]]
SongSpec.member_songs = [
    SongSpec.from_data(data) for data in SongSpec.songs_data["member"]
]
SongSpec.blaster_songs = [
    SongSpec.from_data(data) for data in SongSpec.songs_data["blaster"]
]
SongSpec.pack_songs = [
    PackSongSpec.from_data(data) for data in SongSpec.songs_data["pack"]
]

songs_category_name = "Songs"


def __define_world_spec() -> WorldSpec:
    spec = WorldSpec()

    # region songs

    songs_category = spec.define_category(songs_category_name, starting_count=3)[0]

    def __define_song_list(
        song_list: Iterable[SongSpec],
        other_category: str | None = None,
    ):
        categories = [
            songs_category,
            *([other_category] if other_category != None else []),
        ]

        for song in song_list:
            for chart in song.charts:
                if chart.item_name in spec.items:
                    if other_category:
                        existing = spec.items[chart.item_name]
                        existing["category"] = spec.items[chart.item_name].get(
                            "category", []
                        )
                        existing["category"].append(other_category)
                    continue

                song_item = spec.define_item(
                    chart.item_name,
                    category=categories,
                    progression=True,
                )

                for location_name in chart.location_names:
                    spec.define_location(
                        location_name,
                        category=[
                            *categories,
                            location_name.endswith("Track Clear")
                            and "Goals - Track Clear"
                            or "Goals - Gate Clear",
                        ],
                        requires=Requires.item(song_item),
                    )

    __define_song_list(SongSpec.base_songs)

    member_songs_option = spec.define_toggle_option(
        "enable_member_songs",
        display_name="Enable Membership songs",
        description="Enable songs that require a membership subscription",
        default=False,
    )[0]
    member_songs_category = spec.define_category(
        "Songs - Membership",
        yaml_option=[member_songs_option],
    )[0]
    __define_song_list(SongSpec.member_songs, member_songs_category)

    blaster_songs_option = spec.define_toggle_option(
        "enable_blaster_gate_songs",
        display_name="Enable BLASTER GATE songs",
        description="Enable songs unlocked through BLASTER GATE",
        default=False,
    )[0]
    blaster_songs_category = spec.define_category(
        "Songs - BLASTER GATE",
        yaml_option=[blaster_songs_option],
    )[0]
    __define_song_list(SongSpec.blaster_songs, blaster_songs_category)

    for pack in PackSongSpec.all_song_packs:
        __define_song_list(
            (song for song in SongSpec.pack_songs if song.pack == pack),
            f"Songs - {pack}",
        )

    # endregion songs

    # region other items
    @dataclass
    class ScoreHelperSpec:
        bonus: int  # as x.0000
        count: int
        early: int = 0

    score_helpers = [
        ScoreHelperSpec(bonus=1, count=25, early=5),
        ScoreHelperSpec(bonus=5, count=12, early=1),
        ScoreHelperSpec(bonus=10, count=6),
        ScoreHelperSpec(bonus=20, count=3),
        ScoreHelperSpec(bonus=50, count=1),
    ]

    for score_helper in score_helpers:
        score_helper_item = spec.define_item(
            f"Score +{score_helper.bonus}.0000",
            category=[
                "Helpers - Score (Consume after a play for a score bonus to meet pass requirement)"
            ],
            useful=True,
            count=score_helper.count,
        )

        if score_helper.early > 0:
            score_helper_item["early"] = score_helper.early

    gate_track = ["S", "AAA+", "AAA", "AA+", "AA", "A+", "A", "TRACK CLEAR"]
    gate_item = spec.define_item(
        "Progressive Gate",
        category=[
            f"Progressive Gate (Passing requirement: {", ".join (f"{index + 1} = {item}" for index, item in enumerate(gate_track))})"
        ],
        count=len(gate_track),
        progression=True,
        starting_count=1,
        early=False,
    )

    traps_category = (
        "Traps (The next track must be made with an uncleared trap, then clear it)"
    )
    spec.define_item("Speed 4.0", category=[traps_category], trap=True, count=3)
    spec.define_item("Speed 12.0", category=[traps_category], trap=True, count=3)
    spec.define_item("Random", category=[traps_category], trap=True, count=3)
    spec.define_item("Play First Random", category=[traps_category], trap=True, count=5)

    spec.define_item(
        "Clear Trap",
        category=["Helpers - Clear Trap (Consume to clear a single trap)"],
        useful=True,
        count=10,
        early=3,
    )

    spec.define_item(
        "Song Skip",
        category=[
            "Helpers - Song Skip (Consume to complete a song location without clearing it)"
        ],
        useful=True,
        count=5,
        early=1,
    )

    # endregion other items

    spec.define_location(
        "Finale",
        category="Finale (Pick a boss song to conclude your multiworld!)",
        requires=Requires.all_of(
            Requires.category(songs_category, "70%"),
            Requires.item(gate_item, 5),
        ),
        victory=True,
    )

    return spec


spec = __define_world_spec()
