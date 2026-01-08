from ..lib.helpers import range_inclusive
from ..lib.location import LocationData
from ..lib.world import WorldSpec
from ..lib.requires import Requires


spec = WorldSpec(filler_item_name="Hot Dog")
world_spec = spec

starting_stage_category = spec.define_category(
    "Starting Stage",
    hidden=True,
    starting_count=1,
)[0]

spec.define_item(
    "Stage Skip",
    useful=True,
    count=5,
)

first_place_locations_category = spec.define_category(
    "First Place Locations",
    yaml_option=[
        spec.define_toggle_option(
            "first_place_locations",
            display_name="First Place Locations",
            description="Enable locations which require finishing in first place",
            default=False,
        )[0]
    ],
    hidden=True,
)[0]


# region riders
riders_category = spec.define_category("Riders", starting_count=1)[0]

spec.define_item(
    "Rider Skip",
    category=riders_category,
    useful=True,
    count=5,
)


def define_rider(name: str):
    item = spec.define_item(
        name,
        category=riders_category,
        progression=True,
    )

    spec.define_location(
        f"Play as {name}",
        category=riders_category,
        requires=Requires.item(item),
    )


define_rider("Kirby")
define_rider("King Dedede")
define_rider("Meta Knight")
define_rider("Waddle Dee")
define_rider("Bandana Waddle Dee")
define_rider("Waddle Doo")
define_rider("Chef Kawasaki")
define_rider("Knuckle Joe")
define_rider("Rick")
define_rider("Gooey")
define_rider("Cappy")
define_rider("Rocky")
define_rider("Scarfy")
define_rider("Starman")
define_rider("Lololo & Lalala")
define_rider("Marx")
define_rider("Daroach")
define_rider("Magolor")
define_rider("Taranza")
define_rider("Susie")
define_rider("Noir Dedede")
# endregion riders


# region machines
machines_category = spec.define_category("Machines", starting_count=1)[0]

spec.define_item(
    "Machine Skip",
    category=machines_category,
    useful=True,
    count=5,
)


def define_machine(name: str):
    item = spec.define_item(
        name,
        category=machines_category,
        progression=True,
    )

    spec.define_location(
        f"Ride on {name}",
        category=machines_category,
        requires=Requires.item(item),
    )


define_machine("Warp Star")
define_machine("Compact Star")
define_machine("Winged Star")
define_machine("Shadow Star")
define_machine("Wagon Star")
define_machine("Slick Star")
define_machine("Formula Star")
define_machine("Bulk Star")
define_machine("Rocket Star")
define_machine("Swerve Star")
define_machine("Turbo Star")
define_machine("Jet Star")
define_machine("Wheelie Bike")
define_machine("Rex Wheelie")
define_machine("Wheelie Scooter")
define_machine("Hop Star")
define_machine("Vampire Star")
define_machine("Paper Star")
define_machine("Chariot")
define_machine("Battle Chariot")
define_machine("Tank Star")
define_machine("Bull Tank")
define_machine("Transform Star")
define_machine("Flight Warp Star")
# endregion machines


# region air ride
air_ride_category = spec.define_category("Air Ride")[0]


def define_air_ride_course(name: str):
    course_item = spec.define_item(
        f"{name} (Air Ride)",
        category=[air_ride_category, starting_stage_category],
        progression=True,
    )

    spec.define_location(
        f"Race on {name} (Air Ride)",
        category=[air_ride_category],
        requires=Requires.item(course_item),
    )

    spec.define_location(
        f"Get 1st Place on {name} (Air Ride)",
        category=[air_ride_category, first_place_locations_category],
        requires=Requires.item(course_item),
    )


define_air_ride_course("Floria Fields")
define_air_ride_course("Waveflow Waters")
define_air_ride_course("Airtopia Ruins")
define_air_ride_course("Crystalline Fissure")
define_air_ride_course("Steamgust Forge")
define_air_ride_course("Cavernous Corners")
define_air_ride_course("Cyberion Highway")
define_air_ride_course("Mount Amberfalls")
define_air_ride_course("Galactic Nova")
define_air_ride_course("Fantasy Meadows")
define_air_ride_course("Celestial Valley")
define_air_ride_course("Sky Sands")
define_air_ride_course("Frozen Hillside")
define_air_ride_course("Magma Flows")
define_air_ride_course("Beanstalk Park")
define_air_ride_course("Machine Passage")
define_air_ride_course("Checker Knights")
define_air_ride_course("Nebula Belt")
# endregion air ride


# region top ride
top_ride_category = spec.define_category("Top Ride")[0]


def define_top_ride_course(name: str):
    course_item = spec.define_item(
        f"{name} (Top Ride)",
        category=[top_ride_category, starting_stage_category],
        progression=True,
    )

    spec.define_location(
        f"Race on {name} (Top Ride)",
        category=[top_ride_category],
        requires=Requires.item(course_item),
    )

    spec.define_location(
        f"Get 1st Place on {name} (Top Ride)",
        category=[top_ride_category, first_place_locations_category],
        requires=Requires.item(course_item),
    )


define_top_ride_course("Flower")
define_top_ride_course("Flow")
define_top_ride_course("Air")
define_top_ride_course("Crystal")
define_top_ride_course("Steam")
define_top_ride_course("Cave")
define_top_ride_course("Cyber")
define_top_ride_course("Mountain")
define_top_ride_course("Nova")
# endregion top ride


# region city trial
city_trial_category = spec.define_category("City Trial")[0]

progressive_city_trial_count = 5
progressive_city_trial_extras = 3
progressive_city_trial_item = spec.define_item(
    "Progressive City Trial",
    category=city_trial_category,
    progression=True,
    count=progressive_city_trial_count + progressive_city_trial_extras,
)

progressive_city_trial_progress_item = spec.define_item(
    "Progressive City Trial Progress",
    category=city_trial_category,
    progression=True,
    count=progressive_city_trial_count,
)

for i in range_inclusive(progressive_city_trial_count):
    spec.define_location(
        f"Complete City Trial Game {i}",
        category=city_trial_category,
        requires=Requires.item(progressive_city_trial_item, i),
    )
    spec.define_location(
        f"Complete City Trial Game {i} (Progress Tracking)",
        category=city_trial_category,
        requires=Requires.item(progressive_city_trial_item, i),
        place_item=[progressive_city_trial_progress_item["name"]],
    )

spec.define_location(
    "City Trial Completion",
    category=city_trial_category,
    requires=Requires.item(
        progressive_city_trial_progress_item, progressive_city_trial_count
    ),
    victory=True,
)


def define_stadium(name: str):
    stadium_item = spec.define_item(
        f"{name} (Stadium)",
        category=[city_trial_category, starting_stage_category],
        progression=True,
    )

    spec.define_location(
        f"Finish {name} (Stadium)",
        category=city_trial_category,
        requires=Requires.item(stadium_item),
    )

    spec.define_location(
        f"Get 1st Place in {name} (Stadium)",
        category=[city_trial_category, first_place_locations_category],
        requires=Requires.item(stadium_item),
    )


define_stadium("Air Glider")
define_stadium("Beam Gauntlet")
define_stadium("Big Battle")
define_stadium("Button Rush 1")
define_stadium("Button Rush 2")
define_stadium("Gourmet Race")
define_stadium("High Jump")
define_stadium("Kirby Melee 1")
define_stadium("Kirby Melee 2")
define_stadium("Oval Circuit")
define_stadium("Rail Panic")
define_stadium("Skydive 1")
define_stadium("Skydive 2")
define_stadium("VS. Robo Dedede")
define_stadium("VS. Nightmare")
define_stadium("VS. Marx")
define_stadium("VS. Zero Two")
define_stadium("VS. Gigantes")

for i in range_inclusive(3):
    define_stadium(f"Target Flight {i}")

for i in range_inclusive(4):
    define_stadium(f"Drag Race {i}")

for i in range_inclusive(5):
    define_stadium(f"Dustup Derby {i}")
# endregion city trial


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
