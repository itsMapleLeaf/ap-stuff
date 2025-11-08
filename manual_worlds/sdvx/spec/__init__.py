from dataclasses import dataclass
import re
from typing import ClassVar, Iterable, Literal, NotRequired, TypedDict


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
        def locations(self):
            return [
                SongSpec.ChartLocation("score_pass", self),
                SongSpec.ChartLocation("hp_pass", self),
            ]

        @property
        def location_names(self):
            return {loc.name for loc in self.locations}

    @dataclass
    class ChartLocation:
        type: Literal["score_pass", "hp_pass"]
        chart: "SongSpec.Chart"

        @property
        def name(self):
            type_text = self.type == "hp_pass" and "HP Clear" or "Score Clear"
            return f"{self.chart.song.title} - {self.chart.summary} - {type_text}"


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

song_item_category_name = "Songs"
song_location_category_name = "Song Locations"


def __define_world_spec() -> WorldSpec:
    spec = WorldSpec()

    # region progressive gate
    progressive_gate_category = spec.define_category("Progressive Gate")[0]

    progressive_gate_steps = [
        "S",
        "AAA+",
        "AAA",
        "AA+",
        "AA",
        "A+",
        "A",
        "Any Grade",
    ]

    progressive_gate_item = spec.define_item(
        f"Progressive Gate",
        category=[progressive_gate_category],
        starting_count=1,
        progression=True,
        count=round(len(progressive_gate_steps) * 1.5),  # add some extras just in case
        early=False,
    )

    for step_index, step in enumerate(progressive_gate_steps):
        spec.define_location(
            f"Score Gate: {step}",
            category=[f"Progressive Gate (Track your current score requirement)"],
            requires=Requires.item(progressive_gate_item, step_index + 1),
        )

    spec.define_item(
        "Song Skip",
        category=[
            f"Song Skip (Consume after playing a song to auto-pass a song's locations)"
        ],
        useful=True,
        count=20,
        starting_count=1,
    )
    # endregion progressive gate

    # region songs
    song_item_category = spec.define_category(
        song_item_category_name,
        starting_count=7,
    )[0]

    song_location_category = spec.define_category(
        song_location_category_name,
        hidden=True,
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
                    song_item_category,
                    *([group_category] if group_category != None else []),
                ],
                progression=True,
            )

            for chart in song.charts:
                for chart_location in chart.locations:
                    chart_location = spec.define_location(
                        chart_location.name,
                        category=[
                            song_location_category,
                            *([group_category] if group_category != None else []),
                            f"Songs - {song.title} ({group_category or "Base Songs"})",
                        ],
                        requires=Requires.item(song_item),
                        dont_place_item=(
                            chart_location.type == "score_pass"
                            and [progressive_gate_item["name"]]
                            # or chart_location.type == "hp_pass"
                            # and [progressive_gate_hp_item["name"]]
                            or []
                        ),
                    )

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

    navigators_required = round(len(navigators) * 0.7)
    navigators_category = (
        f"Navigators (Rescue {navigators_required} out of {len(navigators)} to win!)"
    )

    for navigator_name in navigators:
        navigator_item = spec.define_item(
            navigator_name,
            category=[navigators_category],
            progression=True,
        )["name"]
        spec.define_location(
            f"Rescue {navigator_name}",
            category=[navigators_category],
            requires=Requires.item(navigator_item),
        )

    spec.define_location(
        "Rescue GRACE",
        category="Victory (You win! If you like, play a finale song to conclude your playthrough.)",
        requires=Requires.category(navigators_category, navigators_required),
        victory=True,
    )
    # endregion navigators

    spec.define_item(
        f"ANOMALY",
        category=[
            "ANOMALY (Play and clear the first randomly-selected chart within your range)"
        ],
        trap=True,
        count=5,
    )

    return spec


spec = __define_world_spec()
