from dataclasses import dataclass, field
import dataclasses
from typing import ClassVar
from ..lib.helpers import range_inclusive
from ..lib.world import WorldSpec
from ..lib.requires import Requires


spec = WorldSpec(filler_item_name="Hot Dog")
world_spec = spec

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


@dataclass
class RiderSpec:
    name: str
    achievements: list[str] = field(default_factory=list)

    riders: ClassVar[list["RiderSpec"]]


RiderSpec.riders = [
    RiderSpec(
        "Kirby",
        ["Defeat a total of 10 enemies with the Ultra Sword Special"],
    ),
    RiderSpec(
        "King Dedede",
        ["Defeat 10 enemies up close with Hammer attacks in a single race"],
    ),
    RiderSpec("Meta Knight", ["Win against a Lv. 8 or higher CPU"]),
    RiderSpec("Waddle Dee", []),
    RiderSpec(
        "Bandana Waddle Dee",
        ["Destroy 2 boxes within 30 sec. of the start of the match"],
    ),
    RiderSpec("Waddle Doo", ["Hit 2 riders with a single optic-blast attack"]),
    RiderSpec("Chef Kawasaki", []),
    RiderSpec("Knuckle Joe", []),
    RiderSpec("Rick", []),
    RiderSpec("Gooey", []),
    RiderSpec("Cappy", []),
    RiderSpec("Rocky", []),
    RiderSpec("Scarfy", []),
    RiderSpec("Starman", []),
    RiderSpec("Lololo & Lalala", []),
    RiderSpec("Marx", []),
    RiderSpec("Daroach", []),
    RiderSpec("Magolor", []),
    RiderSpec("Taranza", []),
    RiderSpec("Susie", []),
    RiderSpec("Noir Dedede", []),
]

for rider in RiderSpec.riders:
    rider_item = spec.define_item(
        rider.name,
        category=riders_category,
        progression=True,
    )

    spec.define_location(
        f"Finish a stage as {rider.name}",
        category=riders_category,
        requires=Requires.item(rider_item),
    )

    for achievement in rider.achievements:
        spec.define_location(
            f"As {rider.name}: {achievement}",
            category=riders_category,
            requires=Requires.item(rider_item),
        )


@dataclass
class MachineSpec:
    name: str
    achievements: list[str] = field(default_factory=list)

    machines: ClassVar[list["MachineSpec"]]


MachineSpec.machines = [
    MachineSpec("Warp Star"),
    MachineSpec("Winged Star"),
    MachineSpec("Shadow Star"),
    MachineSpec("Wagon Star"),
    MachineSpec("Slick Star"),
    MachineSpec("Formula Star"),
    MachineSpec("Bulk Star"),
    MachineSpec("Rocket Star"),
    MachineSpec("Swerve Star"),
    MachineSpec("Turbo Star"),
    MachineSpec("Jet Star"),
    MachineSpec("Wheelie Bike"),
    MachineSpec("Rex Wheelie"),
    MachineSpec("Wheelie Scooter"),
    MachineSpec("Hop Star"),
    MachineSpec("Vampire Star"),
    MachineSpec("Paper Star"),
    MachineSpec("Chariot"),
    MachineSpec("Battle Chariot"),
    MachineSpec("Tank Star"),
    MachineSpec("Bull Tank"),
    MachineSpec("Transform Star"),
    # MachineSpec("Compact Star"),
    # MachineSpec("Flight Warp Star"),
]

for machine in MachineSpec.machines:
    machine_item = spec.define_item(
        machine.name,
        category=machines_category,
        progression=True,
    )

    spec.define_location(
        f"Finish a stage with {machine.name}",
        category=machines_category,
        requires=Requires.item(machine_item),
    )

    for achievement in machine.achievements:
        spec.define_location(
            f"With {machine.name}: {achievement}",
            category=machines_category,
            requires=Requires.item(machine_item),
        )


@dataclass
class AirRideCourseSpec:
    name: str
    achievements: list[str] = field(default_factory=list)

    courses: ClassVar[list["AirRideCourseSpec"]]


AirRideCourseSpec.courses = [
    AirRideCourseSpec(
        "Floria Fields",
        ["Defeat 2 cart-riding Waddle Dee enemies at the same time"],
    ),
    AirRideCourseSpec(
        "Waveflow Waters",
        ["Defeat an enemy Scarfy without making it mad"],
    ),
    AirRideCourseSpec("Airtopia Ruins"),
    AirRideCourseSpec("Crystalline Fissure"),
    AirRideCourseSpec("Steamgust Forge"),
    AirRideCourseSpec("Cavernous Corners"),
    AirRideCourseSpec("Cyberion Highway"),
    AirRideCourseSpec("Mount Amberfalls"),
    AirRideCourseSpec("Galactic Nova"),
    AirRideCourseSpec("Fantasy Meadows"),
    AirRideCourseSpec("Celestial Valley"),
    AirRideCourseSpec("Sky Sands"),
    AirRideCourseSpec("Frozen Hillside"),
    AirRideCourseSpec("Magma Flows"),
    AirRideCourseSpec("Beanstalk Park"),
    AirRideCourseSpec("Machine Passage"),
    AirRideCourseSpec("Checker Knights"),
    AirRideCourseSpec("Nebula Belt"),
]

for air_ride_course in AirRideCourseSpec.courses:
    air_ride_course_item = spec.define_item(
        air_ride_course.name,
        category=[air_ride_category, starting_stage_category],
        progression=True,
    )

    spec.define_location(
        f"Finish a race on {air_ride_course.name}",
        category=air_ride_category,
        requires=Requires.item(air_ride_course_item),
    )

    for achievement in air_ride_course.achievements:
        spec.define_location(
            f"On {air_ride_course.name}: {achievement}",
            category=air_ride_category,
            requires=Requires.item(air_ride_course_item),
        )


@dataclass
class TopRideCourseSpec:
    name: str
    achievements: list[str] = field(default_factory=list)

    courses: ClassVar[list["TopRideCourseSpec"]]


TopRideCourseSpec.courses = [
    TopRideCourseSpec("Flower"),
    TopRideCourseSpec("Flow"),
    TopRideCourseSpec("Air"),
    TopRideCourseSpec("Crystal"),
    TopRideCourseSpec("Steam"),
    TopRideCourseSpec("Cave"),
    TopRideCourseSpec("Cyber"),
    TopRideCourseSpec("Mountain"),
    TopRideCourseSpec("Nova"),
]

for top_ride_course in TopRideCourseSpec.courses:
    top_ride_course_item = spec.define_item(
        top_ride_course.name,
        category=[top_ride_category, starting_stage_category],
        progression=True,
    )

    spec.define_location(
        f"Finish a race on {top_ride_course.name}",
        category=top_ride_category,
        requires=Requires.item(top_ride_course_item),
    )

    for achievement in top_ride_course.achievements:
        spec.define_location(
            f"On {top_ride_course.name}: {achievement}",
            category=top_ride_category,
            requires=Requires.item(top_ride_course_item),
        )


@dataclass
class StadiumSpec:
    name: str
    count: int = 1
    achievements: list[str] = dataclasses.field(default_factory=list)


stadiums: list[StadiumSpec] = [
    StadiumSpec("Air Glider"),
    StadiumSpec("Beam Gauntlet"),
    StadiumSpec(
        "Big Battle",
        count=2,
        achievements=["Attack a rider while they're enlarged from a Size Up"],
    ),
    StadiumSpec("Button Rush", count=2),
    StadiumSpec("Drag Race", count=4),
    StadiumSpec("Dustup Derby", count=5),
    StadiumSpec("Gourmet Race"),
    StadiumSpec("High Jump"),
    StadiumSpec("Kirby Melee", count=2),
    StadiumSpec("Oval Circuit"),
    StadiumSpec("Rail Panic"),
    StadiumSpec("Skydive", count=2),
    StadiumSpec("Target Flight", count=3),
    StadiumSpec("VS. Robo Dedede"),
    StadiumSpec("VS. Nightmare"),
    StadiumSpec("VS. Marx"),
    StadiumSpec("VS. Zero Two"),
    StadiumSpec("VS. Gigantes"),
]


for stadium_event in stadiums:
    stadium_event_category = spec.define_category(
        f"Stadium - {stadium_event.name}", hidden=True
    )[0]

    for stadium_number in range_inclusive(stadium_event.count):
        stadium_name = stadium_event.name
        if stadium_event.count > 1:
            stadium_name += f" {stadium_number}"

        stadium_event_item = spec.define_item(
            stadium_name,
            category=[
                stadium_category,
                stadium_event_category,
                starting_stage_category,
            ],
            progression=True,
        )

        spec.define_location(
            f"Finish {stadium_name}",
            category=[stadium_category, stadium_event_category],
            requires=Requires.item(stadium_event_item),
        )

    for achievement in stadium_event.achievements:
        spec.define_location(
            f"In {stadium_event.name}: {achievement}",
            category=[stadium_category, stadium_event_category],
            requires=Requires.category(stadium_event_category),
        )


# region city trial
@dataclass
class CityTrialGameSpec:
    max_game_count: ClassVar = 10
    games: ClassVar[list["CityTrialGameSpec"]]

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


CityTrialGameSpec.games = [
    CityTrialGameSpec(number=i)
    for i in range_inclusive(CityTrialGameSpec.max_game_count)
]
# endregion city trial

# region achievements
general_achievements = {
    "Finish while doing a Quick Spin",
    "Finish without using your Special",
    "Finish while flying through the air",
    "Finish without attacking another rider",
    "Finish without riding over any dash zones",
}

air_ride_achievements = {
    "Defeat 3 enemies by spitting out stars in a single race",
    "Defeat 20 enemies in a single race",
    "Inhale or capture 2 enemies at once",
}

city_trial_achievements = {
    "Pass through golden rings 5 times in a single event",
    "Soar 100 m up into the air and fly above the garden in the sky",
    "Swap to vacant machines 5 times in one game",
    "Power up any stat to 12 or higher in a single match",
    "Swap to a vacant duplicate of your current machine",
    "Destroy another rider's machine",
    "Make Whispy Woods cry",
}

for achievement in general_achievements:
    spec.define_location(
        achievement,
        category="Achievements",
    )

for achievement in air_ride_achievements:
    spec.define_location(
        f"Air Ride: {achievement}",
        category="Achievements - Air Ride",
        requires=Requires.category(air_ride_category),
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

    for track_index, track_value in enumerate(track_values):
        spec.define_location(
            f"Progressive {track_name} - {track_value}",
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
