from dataclasses import dataclass, field
import dataclasses
from .songs import Song
from .world import WorldSpec
from .config import song_goals, song_brackets
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

goal_location_count = sum(bracket.count for bracket in song_brackets)

songs_item_category = "Songs"
score_item_count = int(goal_location_count * 0.3)

world_spec = WorldSpec(
    starting_items=[
        {"item_categories": [songs_item_category], "random": 3},
    ],
)

goal_reward_category_name = "Goal Reward"
world_spec.define_category(
    goal_reward_category_name,
    hidden=True,
)

score_item = world_spec.define_item(
    "Score +1.0000 (you tried)",
    count=score_item_count,
    category=["Score Helpers", goal_reward_category_name],
    useful=True,
)

world_spec.define_item(
    "CHAIN",
    category=["CHAIN", goal_reward_category_name],
    progression_skip_balancing=True,
    local=True,
    count=goal_location_count * len(song_goals) - score_item_count,
)

world_spec.define_location(
    "PERFECT ULTIMATE CHAIN",
    category="Victory",
    requires="|CHAIN:50%|",
    victory=True,
)

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

    for song_goal in song_goals:
        song_spec.locations.append(
            world_spec.define_location(
                f"{song_item_name} - {song_goal.name}",
                category=[song_location_category_name, song_spec.id_category_name],
                requires=song_requires,
                place_item_category=[goal_reward_category_name],
            )
        )

spec = world_spec
