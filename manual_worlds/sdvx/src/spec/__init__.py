from dataclasses import dataclass, field
import dataclasses
from .songs import Song
from .world import WorldSpec
from .types import ItemData, LocationData
from ..Helpers import load_data_file


@dataclass
class SongSpec(Song):
    items: list[ItemData] = field(default_factory=list)
    locations: list[LocationData] = field(default_factory=list)

    @property
    def id_category_name(self) -> str:
        return f"Song ID {self.id}"


songs_data: object = load_data_file("songs.json")
if not isinstance(songs_data, list):
    raise Exception("song data must be a list")

all_songs = [Song(**item) for item in songs_data]

# figure out which song titles are duplicated,
# so we can differentiate their item names later
song_titles = set[str]()
duplicate_song_titles = set[str]()
for song in all_songs:
    if not song.title in song_titles:
        song_titles.add(song.title)
    else:
        duplicate_song_titles.add(song.title)


@dataclass
class InclusionBracketSpec:
    min_level: int
    max_level: int
    default: int

    @property
    def option_name(self) -> str:
        return "song_count_level_" + (
            f"{self.min_level}_to_{self.max_level}"
            if self.min_level != self.max_level
            else f"{self.min_level}"
        )

    @property
    def option_display_name(self) -> str:
        return (
            "Song Count (Level "
            + (
                f"{self.min_level} to {self.max_level}"
                if self.min_level != self.max_level
                else f"{self.min_level}"
            )
            + ")"
        )


inclusion_brackets = [
    InclusionBracketSpec(1, 7, default=0),
    InclusionBracketSpec(8, 12, default=0),
    InclusionBracketSpec(13, 15, default=0),
    InclusionBracketSpec(16, 16, default=0),
    InclusionBracketSpec(17, 17, default=20),
    InclusionBracketSpec(18, 18, default=10),
    InclusionBracketSpec(19, 19, default=7),
    InclusionBracketSpec(20, 20, default=3),
]


songs_item_category = "Songs"

world_spec = WorldSpec(
    starting_items=[
        {"item_categories": [songs_item_category], "random": 3},
    ],
)

for inclusion_bracket in inclusion_brackets:
    world_spec.define_range_option(
        inclusion_bracket.option_name,
        type="Range",
        display_name=inclusion_bracket.option_display_name,
        description=[
            "Includes this number of randomly selected songs that have a chart with a level in this range.",
            "You must include at least 1 total song across all song level options.",
        ],
        range_start=0,
        range_end=100,
        default=inclusion_bracket.default,
    )

goal_reward_category_name = "Goal Reward"
world_spec.define_category(
    goal_reward_category_name,
    hidden=True,
)

filler_score_item = world_spec.define_item(
    "Score +1.0000 (you tried)",
    category=["Score Helpers", goal_reward_category_name],
    filler=True,
)

world_spec.define_item(
    "Score +5.0000",
    category=["Score Helpers", goal_reward_category_name],
    useful=True,
    count=20,
)

world_spec.define_item(
    "Score +10.0000",
    category=["Score Helpers", goal_reward_category_name],
    useful=True,
    count=5,
)

world_spec.define_item(
    "CHAIN",
    category=["CHAIN", goal_reward_category_name],
    progression_skip_balancing=True,
    local=True,
)

world_spec.define_location(
    "PERFECT ULTIMATE CHAIN",
    category="Victory",
    requires="|CHAIN:50%|",
    victory=True,
)


@dataclass
class RankLocationSpec:
    name: str

    def __post_init__(self) -> None:
        (self.option_name, self.option) = world_spec.define_toggle_option(
            f"enable_{self.name.lower()}_rank_locations",
            type="Toggle",
            display_name=f"Enable {self.name} rank locations",
            description=[
                f"Enable locations for getting a {self.name} rank or higher.",
                "**At least one rank location must be enabled.**",
            ],
            default=True,
        )

        (self.category_name, self.category) = world_spec.define_category(
            f"Rank {self.name} Locations",
            hidden=True,
            yaml_option=[self.option_name],
        )


rank_locations = [
    RankLocationSpec("A"),
    RankLocationSpec("AA"),
    RankLocationSpec("AAA"),
    RankLocationSpec("S"),
]


song_specs: list[SongSpec] = []


for song in all_songs:
    song_spec = SongSpec(**dataclasses.asdict(song))
    song_specs.append(song_spec)

    world_spec.define_category(
        song_spec.id_category_name,
        hidden=True,
    )

    song_item_name = (
        song.title
        if not song.title in duplicate_song_titles
        else f"{song.title} (by {song.artist})"
    )

    song_location_category_name = f"Songs - {song_item_name}"

    song_spec.items.append(
        world_spec.define_item(
            song_item_name,
            category=[song_spec.id_category_name, songs_item_category],
            progression=True,
        )
    )

    # category requires are expensive for playthrough calculation,
    # so only use them if necessary, such as if the song name
    # would break the require string because sdvx artists
    # can't use normal song titles fkldsjfl
    song_requires = (
        f"|{song_item_name}|"
        if all(char not in song_item_name for char in ":|")
        else f"|@{song_spec.id_category_name}|"
    )

    song_spec.locations.append(
        world_spec.define_location(
            f"{song_item_name} - Track Clear",
            category=[song_location_category_name, song_spec.id_category_name],
            requires=song_requires,
        )
    )

    for rank_location in rank_locations:
        song_spec.locations.append(
            world_spec.define_location(
                f"{song_item_name} - {rank_location.name} Rank or higher",
                category=[
                    song_location_category_name,
                    song_spec.id_category_name,
                    rank_location.category_name,
                ],
                requires=song_requires,
                place_item_category=[goal_reward_category_name],
            )
        )

spec = world_spec
