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

filler_item_name = "sound voltex song effects to sleep and relax to"
filler_item_weight = 7

spec = WorldSpec(
    game="SoundVoltex",
    creator="MapleLeaf",
    filler_item_name=filler_item_name,
)

# backcompat re-export
world_spec = spec

spec.define_toggle_option(
    "converts_only",
    display_name="Only use charts that have converts",
    description="Only include charts that have community converts available. Recommended if you're using a SDVX simulator to play, such as Unnamed SDVX Clone or K-Shoot MANIA.",
    default=False,
)

# region chart level options
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


for chart_level_range_spec in chart_level_range_specs:
    chart_level_range_spec.define_range_option(spec)
# endregion chart level options


# region goal/volforce
goal_total_option_name = spec.define_range_option(
    "volforce_percent",
    display_name="VOLFORCE Percent",
    description=[
        "The percent of VOLFORCE items (victory items) to add to the pool, based on the number of songs (rounded)",
        "e.g. 50 songs * 60% = 30 VOLFORCE items",
    ],
    range_start=10,
    range_end=80,
    default=40,
)[0]

goal_required_option_name = spec.define_range_option(
    "volforce_goal_percent",
    display_name="VOLFORCE Goal Percent",
    description=[
        "The percent of VOLFORCE items required to unlock your goal song (rounded)",
        "e.g. 30 total VOLFORCE * 70% = 21 to win",
    ],
    range_start=50,
    range_end=100,
    default=50,
)[0]

goal_level_option_name = spec.define_range_option(
    "goal_level",
    display_name="Goal Level",
    description=["The level for your goal song"],
    range_start=1,
    range_end=20,
    default=20,
)[0]

goal_category = "Goal"

goal_item_def = spec.define_item(
    "VOLFORCE",
    category=[goal_category],
    progression=True,
)

goal_unlock_def = spec.define_location(
    "GOAL ACCESS",
    category=[goal_category],
    requires="{goal_access()}",
    prehint=True,
)

goal_song_item_def = spec.define_item(
    "PERFECT ULTIMATE CHAIN",
    category=[goal_category],
    progression=True,
)

goal_location_def = spec.define_location(
    "PERFECT ULTIMATE CHAIN",
    requires=Requires.item(goal_song_item_def),
    victory=True,
)
# endregion goal/volforce


# region helpers
helper_percent_option_name = spec.define_range_option(
    "helper_percent",
    display_name="Helper Item Percent",
    description=[
        "Percent of remaining space for AUTO CLEAR items after placing VOLFORCE"
    ],
    range_start=0,
    range_end=100,
    default=50,
)[0]

helper_item_def = spec.define_item(
    "AUTO CLEAR",
    category=["AUTO CLEAR (Consume after play to clear a single song location)"],
    useful=True,
)
# endregion helpers


# region traps
# trap_percent_option_name = spec.define_range_option(
#     "trap_percent",
#     display_name="Helper Item Percent",
#     description=[
#         "Percent of remaining space for trap items (like ANOMALY) after placing VOLFORCE and helper items"
#     ],
#     range_start=0,
#     range_end=100,
#     default=15,
# )[0]
trap_item_def = spec.define_item(
    "ANOMALY",
    category=[
        f"ANOMALY (Play and clear the first randomly-selected chart within your range)"
    ],
    trap=True,
)
# endregion traps


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
    "B",
    "C",
]

progressive_gate_item = spec.define_item(
    f"Progressive Gate",
    category=[progressive_gate_category],
    progression=True,
    count=round(len(progressive_gate_steps)),
    early=False,
)


def zip_with_next[T](iterable: Iterable[T]) -> Iterable[tuple[T, T | None]]:
    iterator = iter(iterable)
    previous = next(iterator)
    for current in iterator:
        yield (previous, current)
        previous = current


for step_index, (step_a, step_b) in enumerate(zip_with_next(progressive_gate_steps)):
    spec.define_location(
        f"Progressive Gate {step_index:02d} - {step_a} -> {step_b}",
        category=[
            f"Progressive Gate (Your first unchecked location is your score clear requirement; check all for any clear)"
        ],
        requires=Requires.item(progressive_gate_item, step_index + 1),
    )

# endregion progressive gate


# region songs
song_item_category = spec.define_category(
    song_item_category_name,
    starting_count=3,
)[0]

song_location_category = spec.define_category(
    song_location_category_name,
    hidden=True,
)[0]


def define_song_list(song_list: Iterable[SongSpec], group_category: str | None = None):
    for song in song_list:
        if song.item_name in spec.items:
            if group_category:
                existing = spec.items[song.item_name]
                existing["category"] = spec.items[song.item_name].get("category", [])
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
