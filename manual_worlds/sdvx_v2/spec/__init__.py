from dataclasses import dataclass
import re
from typing import ClassVar, Iterable, Literal, NotRequired, TypedDict, Unpack

from .types import ItemArgs

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

    @property
    def item_name(self):
        return f"{self.safe_title}"

    @dataclass
    class Chart:
        diff: str
        level: int
        song: "SongSpec"

        @property
        def summary(self):
            return f"{self.diff.upper()} {self.level}"

        @property
        def location_names(self):
            return [
                f"{self.song.title} - {self.summary} - Track Clear",
                f"{self.song.title} - {self.summary} - Gate Clear",
            ]


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

    # region progressive gate
    gate_track = [
        "S Rank",
        "AAA+ Rank",
        "AAA Rank",
        "AA+ Rank",
        "AA Rank",
        "A+ Rank",
        "A Rank",
        "Any Clear",
    ]

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

    for gate_index, requirement in enumerate(gate_track):
        spec.define_location(
            f"Gate: {requirement}",
            category=["Progressive Gate"],
            requires=Requires.item(gate_item, gate_index + 1),
        )
    # endregion progressive gate

    # region songs
    songs_category = spec.define_category(
        songs_category_name,
        starting_count=3,
    )[0]

    def define_song_list(
        song_list: Iterable[SongSpec], group_category: str | None = None
    ):
        for song in song_list:
            if song.item_name in spec.items:
                if group_category:
                    existing = spec.items[song.item_name]
                    existing["category"] = spec.items[song.item_name].get(
                        "category", []
                    )
                    existing["category"].append(group_category)
                continue

            song_item = spec.define_item(
                song.item_name,
                category=[
                    songs_category,
                    *([group_category] if group_category != None else []),
                ],
                progression=True,
            )

            for chart in song.charts:
                for location_name in chart.location_names:
                    chart_location = spec.define_location(
                        location_name,
                        category=[
                            songs_category,
                            *([group_category] if group_category != None else []),
                            f"Songs - {song.title} ({group_category or "Base Songs"})",
                        ],
                        requires=Requires.item(song_item),
                    )

                    if location_name.endswith("Gate Clear"):
                        chart_location["dont_place_item"] = [gate_item["name"]]

    define_song_list(SongSpec.base_songs)

    member_songs_option = spec.define_toggle_option(
        "enable_member_songs",
        display_name="Enable Membership songs",
        description="Enable songs that require a membership subscription",
        default=False,
    )[0]
    member_songs_category = spec.define_category(
        "Membership",
        yaml_option=[member_songs_option],
        hidden=True,
    )[0]
    define_song_list(SongSpec.member_songs, member_songs_category)

    blaster_songs_option = spec.define_toggle_option(
        "enable_blaster_gate_songs",
        display_name="Enable BLASTER GATE songs",
        description="Enable songs unlocked through BLASTER GATE",
        default=False,
    )[0]
    blaster_songs_category = spec.define_category(
        "BLASTER GATE",
        yaml_option=[blaster_songs_option],
        hidden=True,
    )[0]
    define_song_list(SongSpec.blaster_songs, blaster_songs_category)

    for pack in PackSongSpec.all_song_packs:
        (pack_category, _) = spec.define_category(
            pack,
            hidden=True,
        )
        define_song_list(
            (song for song in SongSpec.pack_songs if song.pack == pack),
            pack_category,
        )
    # endregion songs

    # region other items
    def define_score_helper(bonus: int, **args: Unpack[ItemArgs]):  # as x.0000
        args.setdefault(
            "category",
            [
                "Helpers - Score (Consume after a play for a score bonus to meet pass requirement)"
            ],
        )
        spec.define_item(f"Score +{bonus}.0000", **args)

    # define_score_helper(bonus=1, count=25, filler=True)
    # define_score_helper(bonus=5, count=12, filler=True)
    # define_score_helper(bonus=10, count=6, filler=True)
    # define_score_helper(bonus=20, count=3, useful=True)
    # define_score_helper(bonus=50, count=1, useful=True)
    define_score_helper(bonus=1, count=20, filler=True)
    define_score_helper(bonus=5, count=5, filler=True)

    def define_gauge_helper(bonus: int, **args: Unpack[ItemArgs]):  # as x.0000
        args.setdefault(
            "category",
            [
                "Helpers - Gauge (Consume after a play for a health gauge bonus to meet clear requirement)"
            ],
        )
        spec.define_item(f"Gauge +{bonus}%", **args)

    # define_gauge_helper(bonus=1, count=10, filler=True)
    # define_gauge_helper(bonus=2, count=5, filler=True)
    # define_gauge_helper(bonus=5, count=3, useful=True)
    # define_gauge_helper(bonus=10, count=2, useful=True)
    # define_gauge_helper(bonus=20, count=1, useful=True)
    define_gauge_helper(bonus=2, count=20, filler=True)
    define_gauge_helper(bonus=10, count=5, filler=True)

    # mod_traps_category = (
    #     "Mod Traps (The next check must be made with an uncleared trap, then clear it)"
    # )
    # spec.define_item(
    #     "Speed 5.0 (Trap)", category=[mod_traps_category], trap=True, count=2
    # )
    # spec.define_item(
    #     "Speed 10.0 (Trap)", category=[mod_traps_category], trap=True, count=2
    # )
    # spec.define_item("Random (Trap)", category=[mod_traps_category], trap=True)

    blocker_traps_category = (
        "Russian Roulette (Choose random, play whatever comes up first)"
    )
    spec.define_item(
        "Russian Roulette (Normal Clear) (Trap)",
        category=[blocker_traps_category],
        trap=True,
        count=3,
    )
    spec.define_item(
        "Russian Roulette (Gate Clear) (Trap)",
        category=[blocker_traps_category],
        trap=True,
    )

    spec.define_item(
        "Song Skip",
        category=[
            "Helpers - Song Skip (Consume to complete any song's locations, or consume a trap)"
        ],
        useful=True,
        count=7,
    )

    # endregion other items

    # region navigators
    navigators = [
        "RASIS",
        "Tsumabuki RIGHT",
        "Tsumabuki LEFT",
        "TSUMABUKI",
        "TAMA-chan",
        "TAMANEKO",
        "Voltenizer Maxima",
        "NEAR & NOAH",
        "Kanade Yamashina",
        "Kureha",
        "Hina, Ao, and Momo",
        "Kougei Ciel Nana",
        "Lyric Rishuna",
    ]

    navigators_category = "Navigators"
    navigators_required = round(len(navigators) * 0.7)

    for navigator_name in navigators:
        spec.define_item(
            navigator_name,
            category=[navigators_category],
            progression=True,
        )

    spec.define_location(
        "Rescue GRACE",
        category="Victory (You win! If you like, play a finale song to conclude your playthrough.)",
        requires=Requires.all_of(
            Requires.item(gate_item, 5),
            Requires.category(navigators_category, navigators_required),
        ),
        victory=True,
    )
    # endregion navigators

    return spec


spec = __define_world_spec()
