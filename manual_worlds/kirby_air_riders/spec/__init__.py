from dataclasses import InitVar, dataclass
import dataclasses
from itertools import pairwise
from typing import ClassVar
from ..lib.helpers import range_inclusive
from ..lib.world import WorldSpec
from ..lib.requires import Requires


spec = WorldSpec(filler_item_name="Hot Dog")
world_spec = spec


@dataclass
class UnlockableSpec:
    name: str
    categories: list[str]
    location_names: InitVar[list[str]]

    def __post_init__(self, location_names: list[str]):
        self.item = spec.define_item(
            self.name,
            category=self.categories,
            progression=True,
        )
        self.locations = [
            spec.define_location(
                location_name,
                category=self.categories,
                requires=Requires.item(self.item),
            )
            for location_name in location_names
        ]


riders_category = spec.define_category("Players - Riders", starting_count=1)[0]
machines_category = spec.define_category("Players - Machines", starting_count=1)[0]

air_ride_category = spec.define_category("Stages - Air Ride")[0]
top_ride_category = spec.define_category("Stages - Top Ride")[0]
stadium_category = spec.define_category("Stages - Stadium")[0]

city_trial_category = spec.define_category("City Trial")[0]

starting_stage_category = spec.define_category(
    "Starting Stage",
    hidden=True,
    starting_count=1,
)[0]


def define_rider(name: str, achievements: list[str] | None = None) -> UnlockableSpec:
    achievement_list = achievements or []
    return UnlockableSpec(
        name,
        categories=[riders_category],
        location_names=[
            f"Finish a stage as {name}",
            *(f"As {name}: {achievement}" for achievement in achievement_list),
        ],
    )


def define_machine(name: str) -> UnlockableSpec:
    return UnlockableSpec(
        name,
        categories=[machines_category],
        location_names=[f"Finish a stage with {name}"],
    )


def define_air_ride_course(
    name: str, achievements: list[str] | None = None
) -> UnlockableSpec:
    achievement_list = achievements or []
    return UnlockableSpec(
        name,
        categories=[air_ride_category, starting_stage_category],
        location_names=[
            f"Finish a race on {name}",
            *[f"On {name}: {achievement}" for achievement in achievement_list],
        ],
    )


def define_top_ride_course(
    name: str, achievements: list[str] | None = None
) -> UnlockableSpec:
    achievement_list = achievements or []
    return UnlockableSpec(
        name,
        categories=[top_ride_category, starting_stage_category],
        location_names=[
            f"Finish a race on {name}",
            *(f"On {name}: {achievement}" for achievement in achievement_list),
        ],
    )


def define_stadium_event(
    name: str, achievements: list[str] | None = None
) -> UnlockableSpec:
    stadium_event_category = spec.define_category(f"Stadium - {name}", hidden=True)[0]

    return UnlockableSpec(
        name,
        categories=[
            stadium_category,
            stadium_event_category,
            starting_stage_category,
        ],
        location_names=[
            f"Finish {name}",
            *(f"In {name}: {achievement}" for achievement in achievements or []),
        ],
    )


riders = [
    define_rider(
        "Kirby", ["Defeat a total of 10 enemies with the Ultra Sword Special"]
    ),
    define_rider(
        "King Dedede",
        ["Defeat 10 enemies up close with Hammer attacks in a single stage"],
    ),
    define_rider("Meta Knight", ["Win against a Lv. 8 or higher CPU"]),
    define_rider("Waddle Dee"),
    define_rider("Bandana Waddle Dee", ["Defeat another rider with your special"]),
    define_rider("Waddle Doo", ["Hit 2 riders with a single optic-blast attack"]),
    define_rider("Chef Kawasaki"),
    define_rider("Knuckle Joe", ["Defeat another rider with your special"]),
    define_rider("Rick"),
    define_rider("Gooey"),
    define_rider("Cappy"),
    define_rider("Rocky"),
    define_rider("Scarfy"),
    define_rider("Starman"),
    define_rider("Lololo & Lalala"),
    define_rider("Marx"),
    define_rider("Daroach"),
    define_rider("Magolor"),
    define_rider("Taranza"),
    define_rider("Susie"),
    define_rider("Noir Dedede"),
]


machines = [
    define_machine("Warp Star"),
    define_machine("Winged Star"),
    define_machine("Shadow Star"),
    define_machine("Wagon Star"),
    define_machine("Slick Star"),
    define_machine("Formula Star"),
    define_machine("Bulk Star"),
    define_machine("Rocket Star"),
    define_machine("Swerve Star"),
    define_machine("Turbo Star"),
    define_machine("Jet Star"),
    define_machine("Wheelie Bike"),
    define_machine("Rex Wheelie"),
    define_machine("Wheelie Scooter"),
    define_machine("Hop Star"),
    define_machine("Vampire Star"),
    define_machine("Paper Star"),
    define_machine("Chariot"),
    define_machine("Battle Chariot"),
    define_machine("Tank Star"),
    define_machine("Bull Tank"),
    define_machine("Transform Star"),
]


air_ride_courses = [
    define_air_ride_course(
        "Floria Fields", ["Defeat 2 cart-riding Waddle Dee enemies at the same time"]
    ),
    define_air_ride_course(
        "Waveflow Waters", ["Defeat an enemy Scarfy without making it mad"]
    ),
    define_air_ride_course("Airtopia Ruins"),
    define_air_ride_course("Crystalline Fissure"),
    define_air_ride_course("Steamgust Forge"),
    define_air_ride_course("Cavernous Corners"),
    define_air_ride_course("Cyberion Highway"),
    define_air_ride_course("Mount Amberfalls"),
    define_air_ride_course(
        "Galactic Nova", ["Finish after passing through 3 shooting star spots"]
    ),
    define_air_ride_course("Fantasy Meadows"),
    define_air_ride_course("Celestial Valley"),
    define_air_ride_course("Sky Sands"),
    define_air_ride_course("Frozen Hillside"),
    define_air_ride_course("Magma Flows"),
    define_air_ride_course("Beanstalk Park"),
    define_air_ride_course("Machine Passage"),
    define_air_ride_course("Checker Knights"),
    define_air_ride_course("Nebula Belt"),
]


top_ride_courses = [
    define_top_ride_course("Flower"),
    define_top_ride_course("Flow"),
    define_top_ride_course("Air"),
    define_top_ride_course("Crystal"),
    define_top_ride_course(
        "Steam", ["Accelerate using the flipper 5 times in a single race"]
    ),
    define_top_ride_course("Cave"),
    define_top_ride_course("Cyber"),
    define_top_ride_course("Mountain"),
    define_top_ride_course("Nova"),
]


stadiums = [
    define_stadium_event("Air Glider"),
    define_stadium_event(
        "Beam Gauntlet 1", achievements=["Finish without getting hit by a beam"]
    ),
    define_stadium_event(
        "Beam Gauntlet 2", achievements=["Finish without getting hit by a beam"]
    ),
    define_stadium_event(
        "Big Battle 1",
        achievements=["Attack a rider while they're enlarged from a Size Up"],
    ),
    define_stadium_event(
        "Big Battle 2",
        achievements=["Attack a rider while they're enlarged from a Size Up"],
    ),
    define_stadium_event("Button Rush 1"),
    define_stadium_event(
        "Button Rush 2",
        achievements=["Activate 3 buttons at once with a single Lv. 5 Plasma attack"],
    ),
    define_stadium_event("Drag Race 1"),
    define_stadium_event("Drag Race 2"),
    define_stadium_event(
        "Drag Race 3",
        achievements=["Finish within 0:40.00 without ever leaving the ground"],
    ),
    define_stadium_event(
        "Drag Race 4",
        achievements=["Ride over 6 dash zones in a single match without reversing"],
    ),
    define_stadium_event("Dustup Derby 1"),
    define_stadium_event("Dustup Derby 2"),
    define_stadium_event("Dustup Derby 3"),
    define_stadium_event("Dustup Derby 4"),
    define_stadium_event("Dustup Derby 5"),
    define_stadium_event("Gourmet Race"),
    define_stadium_event("High Jump"),
    define_stadium_event("Kirby Melee 1"),
    define_stadium_event("Kirby Melee 2"),
    define_stadium_event("Oval Circuit"),
    define_stadium_event("Rail Panic"),
    define_stadium_event("Skydive 1"),
    define_stadium_event("Skydive 2"),
    define_stadium_event(
        "Target Flight 1",
        achievements=["Get a perfect score of 200 points"],
    ),
    define_stadium_event(
        "Target Flight 2",
        achievements=["Score exactly 70 points in a single match"],
    ),
    define_stadium_event(
        "Target Flight 3",
        achievements=["Get a perfect score of 200 points"],
    ),
    define_stadium_event("VS. Robo Dedede"),
    define_stadium_event("VS. Nightmare"),
    define_stadium_event("VS. Marx"),
    define_stadium_event("VS. Zero Two"),
    define_stadium_event("VS. Gigantes"),
]


# region city trial
@dataclass
class CityTrialGameSpec:
    max_game_count: ClassVar = 10
    city_trial_games: ClassVar[list["CityTrialGameSpec"]]

    progressive_game_item: ClassVar = spec.define_item(
        "Progressive City Trial",
        category=city_trial_category,
        progression=True,
        count=max_game_count,
    )

    completion_item: ClassVar = spec.define_item(
        "City Trial Completion",
        category=city_trial_category,
        progression=True,
    )

    spec.define_location(
        "City Trial Completion",
        category=city_trial_category,
        requires=Requires.item(completion_item),
        victory=True,
    )

    game_count_option: ClassVar = spec.define_range_option(
        "city_trial_game_count",
        display_name="City Trial Game Count",
        description="The number of city trial games you need to play to complete your goal",
        default=5,
        range_start=1,
        range_end=max_game_count,
    )

    number: int

    def __post_init__(self) -> None:
        self.category = spec.define_category(
            f"City Trial Game {self.number}",
            hidden=True,
        )[0]

        self.location = spec.define_location(
            f"Complete City Trial Game {self.number}",
            category=[city_trial_category, self.category],
            requires=Requires.item(self.progressive_game_item, self.number),
        )


city_trial_games = [
    CityTrialGameSpec(number=i)
    for i in range_inclusive(CityTrialGameSpec.max_game_count)
]
# endregion city trial

# region achievements
air_ride_achievements = {
    "Finish while flying through the air",
    "Defeat 3 enemies by spitting out stars in a single race",
    "Defeat 20 enemies in a single race",
    "Finish without using your Special",
    "Inhale or capture 2 enemies at once",
}

top_ride_achievements = {
    "Finish while doing a Quick Spin",
    "Finish without attacking another rider",
    "Finish without riding over any dash zones",
}

city_trial_achievements = {
    "Pass through rings 5 times in a single event",
    "Soar up to the garden in the sky",
    "Swap to vacant machines 5 times in one game",
    "Power up any stat to 12 or higher in a single match",
    "Swap to a vacant duplicate of your current machine",
    "Destroy another rider's machine",
    "Make Whispy Woods cry",
    "Fly far from Skyah and get struck by lightning",
}

for achievement in air_ride_achievements:
    spec.define_location(
        f"Air Ride: {achievement}",
        category="Achievements - Air Ride",
        requires=Requires.category(air_ride_category),
    )

for achievement in top_ride_achievements:
    spec.define_location(
        f"Top Ride: {achievement}",
        category="Achievements - Top Ride",
        requires=Requires.category(top_ride_category),
    )

for achievement in city_trial_achievements:
    spec.define_location(
        f"City Trial: {achievement}",
        category="Achievements - City Trial",
        requires=Requires.item(CityTrialGameSpec.progressive_game_item),
    )

# endregion achievements

# region progression tracks
tracks = {
    # "Lap Count": [f"{i} {i == 1 and 'Lap' or 'Laps'}" for i in range(5, 0, -1)],
    "CPU Level": [f"Level {i}" for i in range(9, 0, -1)],
    # "CPU Handicap": [f"Handicap {i}" for i in range_inclusive(0, 4)],
}

for track_name, track_values in tracks.items():
    track_item = spec.define_item(
        f"Progressive {track_name}",
        category=f"Progressive {track_name}",
        progression=True,
        count=len(track_values) + 3,
    )

    for track_index, (current, next) in enumerate(pairwise(track_values)):
        spec.define_location(
            f"Progressive {track_name}: {current} -> {next}",
            category=f"Progressive {track_name}",
            requires=Requires.item(track_item, track_index + 1),
        )
# endregion progression tracks

# class RoadTripSpec:
#     base_category = spec.define_category(
#         "Road Trip",
#         yaml_option=[
#             spec.define_toggle_option(
#                 "enable_road_trip",
#                 display_name="Enable Road Trip",
#                 description="Enables items and locations for road trip",
#                 default=False,
#                 group="Road Trip",
#             )[0]
#         ],
#     )[0]

#     stage_count = 12
#     stage_tick_count = 20

#     progressive_stages_item = spec.define_item(
#         "Progressive Stages (Road Trip)",
#         category=base_category,
#         progression=True,
#         count=stage_count,
#     )

#     stage_completion_item = spec.define_item(
#         "Road Trip Stage Completion",
#         category=base_category,
#         progression=True,
#         count=stage_count,
#     )

#     spec.define_item(
#         f"Road Trip Shop Slot",
#         category=[base_category],
#         classification_count={
#             "useful + progression": 9,
#             "useful": 3,
#         },
#     )

#     spec.define_range_option(
#         "goal_stage",
#         display_name="Road Trip Goal Stage",
#         description="The stage you need to complete in Road Trip to meet your goal",
#         range_start=1,
#         range_end=12,
#         default=3,
#     )

#     spec.define_location(
#         f"Road Trip Completion",
#         category=base_category,
#         requires="{road_trip_goal()}",
#         victory=True,
#     )

#     for stage_number in range_inclusive(stage_count):
#         stage_category = spec.define_category(
#             f"Road Trip Stage {stage_number}", hidden=True
#         )[0]

#         for tick_number in range_inclusive(stage_tick_count):
#             spec.define_location(
#                 f"Road Trip Progress - Stage {stage_number} - {tick_number} / {stage_tick_count}",
#                 category=[base_category, stage_category],
#                 requires=Requires.item(progressive_stages_item, stage_number),
#             )

#         for stop_number in range_inclusive(3):
#             spec.define_location(
#                 f"Reach Rest Area {stop_number} (Road Trip Stage {stage_number})",
#                 category=[base_category, stage_category],
#                 requires=Requires.item(progressive_stages_item, stage_number),
#             )

#         spec.define_location(
#             f"Complete Road Trip Stage {stage_number}",
#             category=[base_category, stage_category],
#             requires=Requires.item(progressive_stages_item, stage_number),
#             place_item=[stage_completion_item["name"]],
#         )
