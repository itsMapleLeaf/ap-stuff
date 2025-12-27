from ..lib.location import LocationData
from ..lib.world import WorldSpec
from ..lib.requires import Requires


class TemplateWorldSpec(WorldSpec):
    def __init__(self):
        super().__init__()

        self.riders_category = self.define_category("Riders", starting_count=1)[0]
        self.machines_category = self.define_category("Machines", starting_count=1)[0]
        self.air_ride_category = self.define_category("Air Ride", starting_count=1)[0]
        self.top_ride_category = self.define_category("Top Ride", starting_count=1)[0]
        self.stadium_category = self.define_category("Stadium", starting_count=1)[0]
        self.road_trip_category = self.define_category("Road Trip", starting_count=1)[0]

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
        self.define_stadium("Button Rush")
        self.define_stadium("Drag Race")
        self.define_stadium("Dustup Derby")
        self.define_stadium("Gourmet Race")
        self.define_stadium("High Jump")
        self.define_stadium("Kirby Melee")
        self.define_stadium("Oval Circuit")
        self.define_stadium("Rail Panic")
        self.define_stadium("Single Race")
        self.define_stadium("Skydive")
        self.define_stadium("Target Flight")
        self.define_stadium("VS. Boss")
        self.define_stadium("VS. Gigantes")

        self.define_road_trip_content()

    def define_rider(self, name: str):
        item = self.define_item(
            name,
            category=self.riders_category,
            progression=True,
            count=2,
        )

        self.define_location(
            f"Win as {name}",
            category=self.riders_category,
            requires=Requires.item(item),
        )

    def define_machine(self, name: str):
        item = self.define_item(
            name,
            category=self.machines_category,
            progression=True,
            count=2,
        )

        self.define_location(
            f"Win with {name}",
            category=self.machines_category,
            requires=Requires.item(item),
        )

    def define_air_ride_course(self, name: str):
        course_item = self.define_item(
            f"{name} (Air Ride)",
            category=self.air_ride_category,
            progression=True,
        )

        self.define_location(
            f"{name} (Air Ride) - Finish in 1st Place",
            category=self.air_ride_category,
            requires=Requires.item(course_item),
        )

    def define_top_ride_course(self, name: str):
        course_item = self.define_item(
            f"{name} (Top Ride)",
            category=self.top_ride_category,
            progression=True,
        )

        self.define_location(
            f"{name} (Top Ride) - Finish in 1st Place",
            category=self.top_ride_category,
            requires=Requires.item(course_item),
        )

    def define_stadium(self, name: str):
        stadium_item = self.define_item(
            f"{name} (Stadium)",
            category=self.stadium_category,
            progression=True,
        )

        self.define_location(
            f"{name} (Stadium) - Finish",
            category=self.stadium_category,
            requires=Requires.item(stadium_item),
        )

        self.define_location(
            f"{name} (Stadium) - Finish in 1st Place",
            category=self.stadium_category,
            requires=Requires.item(stadium_item),
        )

    def define_road_trip_content(self):
        stage_count = 12
        self.road_trip_stage_item_value_key = "road_trip_stages"

        self.define_item(
            "Progressive Stages (Road Trip)",
            category=self.road_trip_category,
            progression=True,
            count=stage_count + 4,
            value={self.road_trip_stage_item_value_key: 1},
        )

        self.define_range_option(
            "goal_stage",
            display_name="Road Trip Goal Stage",
            description="The stage you need to reach in Road Trip to complete your world",
            range_start=1,
            range_end=12,
            default=5,
        )

        for stage_number in range(1, stage_count + 1):
            for stop_number in range(1, 3 + 1):
                self.define_location(
                    f"Road Trip - Stage {stage_number} - Rest Stop {stop_number}",
                    category=self.road_trip_category,
                    requires=requires_item_value(
                        self.road_trip_stage_item_value_key, stage_number
                    ),
                )

            self.define_location(
                f"Road Trip - Stage {stage_number} - Defeat the Boss",
                category=self.road_trip_category,
                requires=requires_item_value(
                    self.road_trip_stage_item_value_key, stage_number
                ),
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
