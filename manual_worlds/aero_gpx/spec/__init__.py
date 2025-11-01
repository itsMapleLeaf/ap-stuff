from dataclasses import dataclass
from ..lib.world import WorldSpec
from ..lib.requires import Requires


class TemplateWorldSpec(WorldSpec):
    def __init__(self):
        super().__init__(
            game="AeroGPX",
            creator="MapleLeaf",
            filler_item_name="Nothing",
        )

        ticket_item = self.define_item(
            "Ticket",
            category=["Tickets"],
            count=30,
            progression=True,
        )

        self.define_item(
            "Level Skip",
            category=["Level Skips"],
            count=7,
            useful=True,
        )

        self.define_location(
            "Victory",
            requires=Requires.item(ticket_item, "70%"),
            victory=True,
        )

        @dataclass
        class CareerDivisionSpec:
            # required_tickets: int
            levels: list[str]

        career_divisions = {
            "Neutron Division": CareerDivisionSpec(
                # required_tickets=0,
                levels=[
                    "Pilot Tutorial #1",
                    "Race: Figure 8 Circuit",
                    "Race: Starborne Sprint",
                    "Duel with the Devil!",
                    "Race: Slipstream Stepdown",
                    "Test Pilot: Vortex Shredder",
                    "Race: Super Cylinder",
                    "Race: Deadly Straights",
                    "Rising Claymore's Revenge!!",
                    "Grand Prix: Neutron Cup",
                ],
            ),
            "Carbon Division": CareerDivisionSpec(
                # required_tickets=20,
                levels=[
                    "Race: Triple Loop",
                    "Mammoth's Survival!",
                    "Race: Two Dimensions",
                    "Battery Power: Two Dimensions",
                    "Race: Sunset Halfpipe",
                    "Test Pilot: Helix Hawk",
                    "Race: Eremas Double Dive",
                    "Lucid Nightmare Takes Flight",
                    "Race: Fatal Fire Works",
                    "Ryder Kane's Gambit",
                    "Grand Prix: Carbon Cup",
                ],
            ),
            "Solar Division": CareerDivisionSpec(
                # required_tickets=40,
                levels=[
                    "Race: Wavia Funnel Dive",
                    "Race: Burning Rollercoaster",
                    "Drifters Aflame",
                    "Race: Slant City Technique",
                    "Test Pilot: Hydro Blazer",
                    "Race: Slalom Shifts",
                    "Race: Midnight Flight",
                    "Grand Prix: Solar Cup",
                ],
            ),
        }

        (levels_category, _) = self.define_category(
            "Levels",
            starting_count=3,
        )

        for division_name, division in career_divisions.items():
            for level_index, level in enumerate(division.levels):
                level_item = self.define_item(
                    level.replace(":", " -"),
                    category=[levels_category],
                    progression=True,
                )

                for difficulty in ["Standard", "Expert", "Ace Pilot"]:
                    if level.startswith("Grand Prix:"):
                        for track_index in range(5):
                            self.define_location(
                                f"{level} - Track {track_index + 1} - {difficulty} Difficulty",
                                category=[
                                    f"Career - {division_name} {level_index + 1:02d} - {level}"
                                ],
                                # requires=Requires.item(ticket_item, division.required_tickets),
                                requires=Requires.item(level_item),
                            )
                    else:
                        self.define_location(
                            f"{level} - {difficulty} Difficulty",
                            category=[
                                f"Career - {division_name} {level_index + 1:02d} - {level}"
                            ],
                            # requires=Requires.item(ticket_item, division.required_tickets),
                            requires=Requires.item(level_item),
                        )

        machines = {
            "Balanced": [
                "Crimson Strider",
                "Lucid Nightmare",
                "Hydro Blazer",
                "Starfire Fury",
            ],
            "Top Speed": [
                "Misty Lady",
                "Devil Dagger",
                "Wicked Motor",
                "Nightshade Streak",
            ],
            "Sliding": [
                "Silken Speeder",
                "Ivory Mako",
                "Wistful Ghost",
                "Slip Shifter",
            ],
            "Flight": [
                "Passion Kite",
                "Vortex Shredder",
                "Helix Hawk",
                "Divine Drake",
            ],
            "Combat": [
                "Sunlit Warrior",
                "Rising Claymore",
                "Eternal Mammoth",
                "Sonic Marauder",
            ],
        }

        (machine_category, _) = self.define_category(
            "Machines",
            hidden=True,
            starting_count=1,
        )

        for machine_type, machine_list in machines.items():
            for machine in machine_list:
                self.define_item(
                    machine,
                    category=[machine_category, f"Machines - {machine_type}"],
                    useful=True,
                )


world_spec = TemplateWorldSpec()
