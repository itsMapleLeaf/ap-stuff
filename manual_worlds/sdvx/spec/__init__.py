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


filler_item_name = "Placeholder (If you see this, there's a bug)"

song_skip_item_name = "Song Skip"
song_skip_item_weight = 8

anomaly_item_name = "ANOMALY"
anomaly_item_weight = 1


@dataclass
class ChartLevelRangeSpec:
    start: int
    end: int
    default: int

    @property
    def option_name(self) -> str:
        if self.start != self.end:
            return f"include_charts_level_{self.start}_to_{self.end}"
        else:
            return f"include_charts_level_{self.start}"

    def define_range_option(self, spec: WorldSpec) -> None:
        spec.define_range_option(
            self.option_name,
            description=(
                f"Include this many charts"
                + (
                    f" from level {self.start} to {self.end}"
                    if self.start != self.end
                    else f" at level {self.start}"
                )
                + "\n\n"
                + "You can specify a random number of charts with `random-range-#-#`, example:"
                + "\n\n"
                + "random-range-5-15: 50"
                + "\n\n"
                + "(And make sure you remove all other keys, or set them to 0!)"
            ),
            range_start=0,
            range_end=100,
            default=self.default,
        )


chart_level_range_specs = [
    ChartLevelRangeSpec(start=1, end=7, default=0),
    ChartLevelRangeSpec(start=8, end=12, default=0),
    ChartLevelRangeSpec(start=13, end=16, default=0),
    ChartLevelRangeSpec(start=17, end=17, default=15),
    ChartLevelRangeSpec(start=18, end=18, default=20),
    ChartLevelRangeSpec(start=19, end=19, default=10),
    ChartLevelRangeSpec(start=20, end=20, default=5),
]


def __define_world_spec() -> WorldSpec:
    spec = WorldSpec(
        game="SoundVoltex",
        creator="MapleLeaf",
        filler_item_name=filler_item_name,
    )

    for chart_level_range_spec in chart_level_range_specs:
        chart_level_range_spec.define_range_option(spec)

    # region chain/victory
    @dataclass
    class ChainSpec:
        count: int
        value: int

    chain_specs = {
        "NEAR": ChainSpec(count=20, value=1),  # 20
        "CRITICAL": ChainSpec(count=8, value=5),  # 40
        "S-CRITICAL": ChainSpec(count=3, value=20),  # 60
    }

    chain_required = 60

    chain_item_category = spec.define_category("CHAIN (Victory item)")[0]

    for chain_spec_name, chain_spec in chain_specs.items():
        spec.define_item(
            f"{chain_spec_name} (CHAIN {chain_spec.value})",
            category=[chain_item_category],
            progression=True,
            count=chain_spec.count,
            value={"CHAIN": chain_spec.value},
        )

    spec.define_location(
        "WORLD CLEAR",
        category=[f"Victory (Collect {chain_required} total CHAIN to win)"],
        requires=f"{{ItemValue(CHAIN:{chain_required})}}",
        victory=True,
    )

    spec.define_location(
        "ULTIMATE CHAIN",
        category=[f"Victory (Collect ALL CHAIN items)"],
        requires=Requires.category(chain_item_category, "all"),
    )
    # endregion chain/victory

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
    ]

    progressive_gate_item = spec.define_item(
        f"Progressive Gate",
        category=[progressive_gate_category],
        progression=True,
        count=round(len(progressive_gate_steps) * 1.5),  # add some extras just in case
        early=False,
    )

    for step_index, step in enumerate(progressive_gate_steps):
        spec.define_location(
            f"Progressive Gate {step_index:02d} - {step}",
            category=[
                f"Progressive Gate (Your first unchecked location is your score clear requirement; check all for any clear)"
            ],
            requires=Requires.item(progressive_gate_item, step_index + 1),
        )

    # endregion progressive gate

    # region helper items
    spec.define_item(
        song_skip_item_name,
        category=[
            f"{song_skip_item_name} (Consume after playing a song to auto-pass a song's locations)"
        ],
        useful=True,
        starting_count=1,
    )
    # endregion helper items

    # region traps
    spec.define_item(
        anomaly_item_name,
        category=[
            f"{anomaly_item_name} (Play and clear the first randomly-selected chart within your range)"
        ],
        trap=True,
    )
    # endregion traps

    # region songs
    song_item_category = spec.define_category(
        song_item_category_name,
        starting_count=5,
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

    return spec


spec = __define_world_spec()
