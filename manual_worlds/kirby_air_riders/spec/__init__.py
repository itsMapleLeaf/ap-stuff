from ..lib.helpers import range_inclusive
from ..lib.location import LocationData
from ..lib.world import WorldSpec
from ..lib.requires import Requires


class TemplateWorldSpec(WorldSpec):
    def __init__(self):
        super().__init__()

        self.riders_category = self.define_category("Riders", starting_count=1)[0]
        self.machines_category = self.define_category("Machines", starting_count=1)[0]

        self.starting_stage_category = self.define_category(
            "Starting Stage", hidden=True, starting_count=1
        )[0]

        self.air_ride_category = self.define_category("Air Ride")[0]
        self.top_ride_category = self.define_category("Top Ride")[0]
        self.stadium_category = self.define_category("Stadium")[0]
        self.road_trip_category = self.define_category("Road Trip")[0]

        self.first_place_locations_category = self.define_category(
            "First Place Locations",
            yaml_option=[
                self.define_toggle_option(
                    "first_place_locations",
                    display_name="First Place Locations",
                    description="Enable locations which require finishing in first place",
                    default=False,
                )[0]
            ],
            hidden=True,
        )[0]

        self.define_item(
            "Stage Skip",
            useful=True,
            count=20,
        )

        self.define_rider("Kirby")
        self.define_rider("King Dedede")
        self.define_rider("Meta Knight")
        self.define_rider("Waddle Dee")
        self.define_rider("Bandana Waddle Dee")
        self.define_rider("Waddle Doo")
        self.define_rider("Chef Kawasaki")
        self.define_rider("Knuckle Joe")
        self.define_rider("Rick")
        self.define_rider("Gooey")
        self.define_rider("Cappy")
        self.define_rider("Rocky")
        self.define_rider("Scarfy")
        self.define_rider("Starman")
        self.define_rider("Lololo & Lalala")
        self.define_rider("Marx")
        self.define_rider("Daroach")
        self.define_rider("Magolor")
        self.define_rider("Taranza")
        self.define_rider("Susie")
        self.define_rider("Noir Dedede")

        self.define_machine("Warp Star")
        self.define_machine("Compact Star")
        self.define_machine("Winged Star")
        self.define_machine("Shadow Star")
        self.define_machine("Wagon Star")
        self.define_machine("Slick Star")
        self.define_machine("Formula Star")
        self.define_machine("Bulk Star")
        self.define_machine("Rocket Star")
        self.define_machine("Swerve Star")
        self.define_machine("Turbo Star")
        self.define_machine("Jet Star")
        self.define_machine("Wheelie Bike")
        self.define_machine("Rex Wheelie")
        self.define_machine("Wheelie Scooter")
        self.define_machine("Hop Star")
        self.define_machine("Vampire Star")
        self.define_machine("Paper Star")
        self.define_machine("Chariot")
        self.define_machine("Battle Chariot")
        self.define_machine("Tank Star")
        self.define_machine("Bull Tank")
        self.define_machine("Transform Star")
        self.define_machine("Flight Warp Star")

        self.define_air_ride_course("Floria Fields")
        self.define_air_ride_course("Waveflow Waters")
        self.define_air_ride_course("Airtopia Ruins")
        self.define_air_ride_course("Crystalline Fissure")
        self.define_air_ride_course("Steamgust Forge")
        self.define_air_ride_course("Cavernous Corners")
        self.define_air_ride_course("Cyberion Highway")
        self.define_air_ride_course("Mount Amberfalls")
        self.define_air_ride_course("Galactic Nova")
        self.define_air_ride_course("Fantasy Meadows")
        self.define_air_ride_course("Celestial Valley")
        self.define_air_ride_course("Sky Sands")
        self.define_air_ride_course("Frozen Hillside")
        self.define_air_ride_course("Magma Flows")
        self.define_air_ride_course("Beanstalk Park")
        self.define_air_ride_course("Machine Passage")
        self.define_air_ride_course("Checker Knights")
        self.define_air_ride_course("Nebula Belt")

        self.define_top_ride_course("Flower")
        self.define_top_ride_course("Flow")
        self.define_top_ride_course("Air")
        self.define_top_ride_course("Crystal")
        self.define_top_ride_course("Steam")
        self.define_top_ride_course("Cave")
        self.define_top_ride_course("Cyber")
        self.define_top_ride_course("Mountain")
        self.define_top_ride_course("Nova")

        self.define_stadium("Air Glider")
        self.define_stadium("Beam Gauntlet")
        self.define_stadium("Big Battle")
        self.define_stadium("Button Rush 1")
        self.define_stadium("Button Rush 2")
        self.define_stadium("Gourmet Race")
        self.define_stadium("High Jump")
        self.define_stadium("Kirby Melee 1")
        self.define_stadium("Kirby Melee 2")
        self.define_stadium("Oval Circuit")
        self.define_stadium("Rail Panic")
        # self.define_stadium("Single Race")
        self.define_stadium("Skydive 1")
        self.define_stadium("Skydive 2")
        self.define_stadium("VS. Robo Dedede")
        self.define_stadium("VS. Nightmare")
        self.define_stadium("VS. Marx")
        self.define_stadium("VS. Zero Two")
        self.define_stadium("VS. Gigantes")

        for i in range_inclusive(3):
            self.define_stadium(f"Target Flight {i}")

        for i in range_inclusive(4):
            self.define_stadium(f"Drag Race {i}")

        for i in range_inclusive(5):
            self.define_stadium(f"Dustup Derby {i}")

        self.define_road_trip_content()

    def define_rider(self, name: str):
        item = self.define_item(
            name,
            category=self.riders_category,
            progression=True,
        )

        self.define_location(
            f"Play as {name}",
            category=self.riders_category,
            requires=Requires.item(item),
        )

    def define_machine(self, name: str):
        item = self.define_item(
            name,
            category=self.machines_category,
            progression=True,
        )

        self.define_location(
            f"Ride on {name}",
            category=self.machines_category,
            requires=Requires.item(item),
        )

    def define_air_ride_course(self, name: str):
        course_item = self.define_item(
            f"{name} (Air Ride)",
            category=[self.air_ride_category, self.starting_stage_category],
            progression=True,
        )

        self.define_location(
            f"Race on {name} (Air Ride)",
            category=[self.air_ride_category],
            requires=Requires.item(course_item),
        )

        self.define_location(
            f"Get 1st Place on {name} (Air Ride)",
            category=[self.air_ride_category, self.first_place_locations_category],
            requires=Requires.item(course_item),
        )

    def define_top_ride_course(self, name: str):
        course_item = self.define_item(
            f"{name} (Top Ride)",
            category=[self.top_ride_category, self.starting_stage_category],
            progression=True,
        )

        self.define_location(
            f"Race on {name} (Top Ride)",
            category=[self.top_ride_category],
            requires=Requires.item(course_item),
        )

        self.define_location(
            f"Get 1st Place on {name} (Top Ride)",
            category=[self.top_ride_category, self.first_place_locations_category],
            requires=Requires.item(course_item),
        )

    def define_stadium(self, name: str):
        stadium_item = self.define_item(
            f"{name} (Stadium)",
            category=[self.stadium_category, self.starting_stage_category],
            progression=True,
        )

        self.define_location(
            f"Finish {name} (Stadium)",
            category=self.stadium_category,
            requires=Requires.item(stadium_item),
        )

        self.define_location(
            f"Get 1st Place in {name} (Stadium)",
            category=[self.stadium_category, self.first_place_locations_category],
            requires=Requires.item(stadium_item),
        )

    def define_road_trip_content(self):
        stage_count = 12
        self.road_trip_stage_item_value_key = "road_trip_stages"

        self.progressive_stages_item = self.define_item(
            "Progressive Stages (Road Trip)",
            category=self.road_trip_category,
            progression=True,
            count=stage_count,
        )

        self.define_range_option(
            "goal_stage",
            display_name="Road Trip Goal Stage",
            description="The stage you need to complete in Road Trip to meet your goal",
            range_start=1,
            range_end=12,
            default=3,
        )

        self.road_trip_completion_item = self.define_item(
            "Road Trip Completion",
            category=self.road_trip_category,
            progression=True,
            count=stage_count,
        )

        for stage_number in range_inclusive(stage_count):
            for stop_number in range_inclusive(3):
                self.define_location(
                    f"Road Trip - Stage {stage_number} - Rest Stop {stop_number}",
                    category=self.road_trip_category,
                    requires=Requires.item(self.progressive_stages_item, stage_number),
                )

            self.define_location(
                f"Road Trip - Stage {stage_number} - Defeat the Boss",
                category=self.road_trip_category,
                requires=Requires.item(self.progressive_stages_item, stage_number),
                place_item=[self.road_trip_completion_item["name"]],
            )

        self.define_location(
            f"Road Trip Completion",
            category=self.road_trip_category,
            requires="{road_trip_goal()}",
            victory=True,
        )


def requires_item_value(key: str, value: str | int):
    return f"{{ItemValue({key}:{value})}}"


def requires_yaml_compare(option_name: str, op: str, value: str | int):
    return f"{{YamlCompare({option_name} {op} {value})}}"


world_spec = TemplateWorldSpec()
