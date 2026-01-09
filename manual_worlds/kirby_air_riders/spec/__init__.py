from typing import cast
from BaseClasses import MultiWorld
from ..lib.item import ItemData
from ..lib.helpers import range_inclusive
from ..lib.location import LocationData
from ..lib.world import WorldSpec
from ..lib.requires import Requires


riders = [
    "Kirby",
    "King Dedede",
    "Meta Knight",
    "Waddle Dee",
    "Bandana Waddle Dee",
    "Waddle Doo",
    "Chef Kawasaki",
    "Knuckle Joe",
    "Rick",
    "Gooey",
    "Cappy",
    "Rocky",
    "Scarfy",
    "Starman",
    "Lololo & Lalala",
    "Marx",
    "Daroach",
    "Magolor",
    "Taranza",
    "Susie",
    "Noir Dedede",
]

machines = [
    "Warp Star",
    "Compact Star",
    "Winged Star",
    "Shadow Star",
    "Wagon Star",
    "Slick Star",
    "Formula Star",
    "Bulk Star",
    "Rocket Star",
    "Swerve Star",
    "Turbo Star",
    "Jet Star",
    "Wheelie Bike",
    "Rex Wheelie",
    "Wheelie Scooter",
    "Hop Star",
    "Vampire Star",
    "Paper Star",
    "Chariot",
    "Battle Chariot",
    "Tank Star",
    "Bull Tank",
    "Transform Star",
    "Flight Warp Star",
]

air_ride_courses = [
    "Floria Fields",
    "Waveflow Waters",
    "Airtopia Ruins",
    "Crystalline Fissure",
    "Steamgust Forge",
    "Cavernous Corners",
    "Cyberion Highway",
    "Mount Amberfalls",
    "Galactic Nova",
    "Fantasy Meadows",
    "Celestial Valley",
    "Sky Sands",
    "Frozen Hillside",
    "Magma Flows",
    "Beanstalk Park",
    "Machine Passage",
    "Checker Knights",
    "Nebula Belt",
]

top_ride_courses = [
    "Flower",
    "Flow",
    "Air",
    "Crystal",
    "Steam",
    "Cave",
    "Cyber",
    "Mountain",
    "Nova",
]

stadiums = [
    "Air Glider",
    "Beam Gauntlet",
    "Big Battle",
    "Button Rush 1",
    "Button Rush 2",
    "Gourmet Race",
    "High Jump",
    "Kirby Melee 1",
    "Kirby Melee 2",
    "Oval Circuit",
    "Rail Panic",
    "Skydive 1",
    "Skydive 2",
    "VS. Robo Dedede",
    "VS. Nightmare",
    "VS. Marx",
    "VS. Zero Two",
    "VS. Gigantes",
    *(f"Target Flight {i}" for i in range_inclusive(3)),
    *(f"Drag Race {i}" for i in range_inclusive(4)),
    *(f"Dustup Derby {i}" for i in range_inclusive(5)),
]


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


for rider in riders:
    spec.define_location(
        f"Finish a Stage as {rider}",
        category=riders_category,
        requires=Requires.item(
            spec.define_item(
                rider,
                category=riders_category,
                progression=True,
            )
        ),
    )

for machine in machines:
    spec.define_location(
        f"Finish a Stage with {machine}",
        category=machines_category,
        requires=Requires.item(
            spec.define_item(
                machine,
                category=machines_category,
                progression=True,
            )
        ),
    )

for air_ride_course in air_ride_courses:
    spec.define_location(
        f"Finish a Race on {air_ride_course}",
        category=air_ride_category,
        requires=Requires.item(
            spec.define_item(
                air_ride_course,
                category=[air_ride_category, starting_stage_category],
                progression=True,
            )
        ),
    )

for top_ride_course in top_ride_courses:
    spec.define_location(
        f"Finish a Race on {top_ride_course}",
        category=top_ride_category,
        requires=Requires.item(
            spec.define_item(
                top_ride_course,
                category=[top_ride_category, starting_stage_category],
                progression=True,
            )
        ),
    )

for stadium in stadiums:
    spec.define_location(
        f"Finish {stadium}",
        category=stadium_category,
        requires=Requires.item(
            spec.define_item(
                stadium,
                category=[stadium_category, starting_stage_category],
                progression=True,
            )
        ),
    )


# region city trial
class CityTrialSpec:
    max_game_count = 10

    progressive_game_item_extras = 3
    progressive_game_item = spec.define_item(
        "Progressive City Trial",
        category=city_trial_category,
        progression=True,
        count=max_game_count + progressive_game_item_extras,
    )

    progress_item = spec.define_item(
        "City Trial Progress",
        category=city_trial_category,
        progression=True,
        count=max_game_count,
    )

    spec.define_location(
        "City Trial Completion",
        category=city_trial_category,
        requires=Requires.item(progress_item, "all"),
        victory=True,
    )

    games: list["CityTrialGameSpec"]

    game_count_option_name = spec.define_range_option(
        "city_trial_game_count",
        display_name="City Trial Game Count",
        description="The number of city trial games you need to play to complete your goal",
        default=5,
        range_start=1,
        range_end=max_game_count,
    )[0]

    @staticmethod
    def get_game_count_option_value(multi: MultiWorld, player: int) -> int:
        from ..Helpers import get_option_value

        return cast(
            int, get_option_value(multi, player, CityTrialSpec.game_count_option_name)
        )


class CityTrialGameSpec:
    def __init__(self, number: int) -> None:
        self.number = number

        self.category = spec.define_category(
            f"City Trial Game {number}",
            hidden=True,
        )[0]

        self.locations = [
            spec.define_location(
                f"Complete City Trial Game {number}",
                category=[city_trial_category, self.category],
                requires=Requires.item(CityTrialSpec.progressive_game_item, number),
            ),
            spec.define_location(
                f"Complete City Trial Game {number} (Progress Tracking)",
                category=[city_trial_category, self.category],
                requires=Requires.item(CityTrialSpec.progressive_game_item, number),
                place_item=[CityTrialSpec.progress_item["name"]],
            ),
        ]


CityTrialSpec.games = [
    CityTrialGameSpec(number=i) for i in range_inclusive(CityTrialSpec.max_game_count)
]

# endregion city trial

general_achievements = {
    "Defeat 3 enemies by spitting out stars in a single race",
    "Defeat an enemy Scarfy without making it mad",
    "Defeat 20 enemies in a single race",
    "Finish while doing a Quick Spin",
    "Inhale or capture 2 enemies at once",
    "Finish without using your Special",
    "Finish while flying through the air",
    "Attack a rider while they're enlarged from a Size Up",
    "Finish without attacking a rider",
    "Finish without riding over any dash zones",
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

for achievement in city_trial_achievements:
    spec.define_location(
        f"City Trial: {achievement}",
        category="Achievements - City Trial",
        requires=Requires.item(CityTrialSpec.progressive_game_item),
    )

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
