from dataclasses import dataclass
from itertools import chain
import re
from typing import ClassVar, Iterable, Literal, NotRequired, TypedDict
from ..lib.requires import Requires
from ..Helpers import load_data_file
from ..lib.world import WorldSpec


class SongData(TypedDict):
    title: str
    # artist: str
    # bpm: str
    nov: float
    adv: float
    exh: float
    mxm: float


@dataclass
class SongSpec:
    title: str
    # artist: str
    charts: list["Chart"]

    type Difficulty = Literal["nov", "adv", "exh", "mxm"]
    diffs: ClassVar[list[Difficulty]] = ["nov", "adv", "exh", "mxm"]

    all_songs: ClassVar[list["SongSpec"]]

    @staticmethod
    def from_data(data: SongData) -> "SongSpec":
        spec = SongSpec(
            title=data["title"],
            # artist=data["artist"],
            charts=[],
        )

        for diff in SongSpec.diffs:
            if diff in data and isinstance(data[diff], float):
                spec.charts.append(
                    SongSpec.Chart(diff=diff, level=data[diff], song=spec)
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
        level: float
        song: "SongSpec"

        @property
        def summary(self):
            return f"{self.diff.upper()} {self.level:g}"

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


SongSpec.all_songs = [SongSpec.from_data(song) for song in load_data_file("songs.json")]


song_item_category_name = "Songs"
song_location_category_name = "Song Locations"

filler_item_name = "sound voltex effects to sleep and relax to"
filler_item_weight = 7

spec = WorldSpec(
    game="SoundVoltex",
    creator="MapleLeaf",
    filler_item_name=filler_item_name,
)

# backcompat re-export
world_spec = spec


simulator_option = spec.define_toggle_option(
    "simulator",
    group="Songs",
    display_name="Using simulator",
    description="Enable this option if you're using a SDVX simulator to play, such as Unnamed SDVX Clone or K-Shoot MANIA. This will make the entire song library available, but only charts that have community converts available.",
    default=False,
)

# region goal/volforce
volforce_count_option_name = spec.define_range_option(
    "volforce_count",
    display_name="VOLFORCE Count",
    description=["The number of VOLFORCE items to add to the pool"],
    group="Goal / VOLFORCE",
    range_start=0,
    range_end=100,
    default=30,
).name

required_volforce_option_name = spec.define_range_option(
    "required_volforce_percent",
    display_name="Required VOLFORCE for goal",
    description=["The percentage of VOLFORCE items required to unlock your goal song"],
    group="Goal / VOLFORCE",
    range_start=0,
    range_end=100,
    default=50,
).name

volforce_item_def = spec.define_item(
    "VOLFORCE",
    category=["VOLFORCE"],
    progression=True,
)

goal_access_def = spec.define_location(
    "GOAL ACCESS",
    category=[
        "GOAL ACCESS (Check this location when it's in logic to unlock your goal song)"
    ],
    requires="{goal_access()}",
    prehint=True,
)

victory_item_def = spec.define_item(
    "PERFECT ULTIMATE CHAIN",
    category=["PERFECT ULTIMATE CHAIN (Victory!)"],
    progression=True,
)

victory_location_def = spec.define_location(
    "PERFECT ULTIMATE CHAIN",
    category=["PERFECT ULTIMATE CHAIN (Victory!)"],
    requires=Requires.item(victory_item_def),
    victory=True,
)
# endregion goal/volforce


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


for song in SongSpec.all_songs:
    if song.item_name in spec.items:
        continue

    song_item = spec.define_item(
        song.item_name,
        category=[
            song_item_category,
        ],
        progression=True,
    )

    for chart in song.charts:
        for chart_location in chart.locations:
            chart_location = spec.define_location(
                chart_location.name,
                category=[
                    song_location_category,
                    f"Songs - {song.title}",
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
# endregion songs


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
            group="Chart Levels",
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

goal_level_option_name = spec.define_range_option(
    "goal_level",
    display_name="Goal Level",
    description=["The level for your goal song"],
    group="Chart Levels",
    range_start=1,
    range_end=20,
    default=20,
).name
# endregion chart level options


# region helpers
helper_count_option_name = spec.define_range_option(
    "helper_count",
    display_name="Helper Item Count",
    description=["Number of AUTO CLEAR items to add to the pool"],
    group="Helpers",
    range_start=0,
    range_end=50,
    default=12,
).name

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
