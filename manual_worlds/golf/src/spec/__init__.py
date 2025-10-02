from .requires import Requires
from .world import WorldSpec


spec = WorldSpec()

courses = [
    "Forest",
    "Haunted",
    "Oasis",
    "Space Station",
    "Museum",
    "Pirate Cove",
    "Volcano",
    "Ancient",
    "Twilight",
    "Candyland",
    "Worms",
    "The Escapists",
    "The Deep",
]

victory_item = spec.define_item(
    "Lost Ball",
    category="Lost Balls",
    count=30,
    progression=True,
)

spec.define_location(
    "Find all the lost balls",
    category="Victory",
    requires=Requires.item(victory_item, "80%"),
    victory=True,
)

course_progressive_item_count = 10
required_course_item_count = 5

course_item_category = f"Courses ({required_course_item_count} Needed)"


def get_course_item_name(course: str) -> str:
    return f"{course} (Progressive Courses)"


for course in courses:
    course_item = spec.define_item(
        get_course_item_name(course),
        category=course_item_category,
        progression=True,
        count=course_progressive_item_count,
    )

    spec.define_location(
        f"{course} - Hole in One!",
        category=f"Courses - {course}",
        requires=Requires.item(course_item, required_course_item_count),
    )

    for hole in range(1, 18 + 1):
        course_hole_location = spec.define_location(
            f"{course} - Hole {hole}",
            category=f"Courses - {course}",
            requires=Requires.item(course_item, required_course_item_count),
        )

# region upgrades
spec.define_item(
    "Max Time +10s",
    category="Upgrades",
    useful=True,
    count=24,
    early=3,
    starting_count=3,
)

spec.define_item(
    "Max Shots +1",
    category="Upgrades",
    useful=True,
    count=15,
    early=3,
    starting_count=6,
)

spec.define_item(
    "Free-cam Time +2s",
    category="Upgrades",
    useful=True,
    count=15,
)

spec.define_item("Retry Shot", category="Upgrades", useful=True, count=2)
spec.define_item("Ball Spin", category="Upgrades", useful=True, count=2)
spec.define_item("Jumping", category="Upgrades", useful=True, count=2)
spec.define_item("Spiking", category="Upgrades", useful=True, count=2)
spec.define_item("Handbrake", category="Upgrades", useful=True, count=2)
spec.define_item("Show Last Power", category="Upgrades", useful=True, count=2)
# endregion upgrades

# region traps
spec.define_item("Gravity 0.25", category="Traps", trap=True, count=3)
spec.define_item("Gravity 0.5", category="Traps", trap=True, count=3)
spec.define_item("Gravity 0.75", category="Traps", trap=True, count=3)

spec.define_item("Egg Ball", category="Traps", trap=True)
spec.define_item("Cube Ball", category="Traps", trap=True)
spec.define_item("Cylinder Ball", category="Traps", trap=True)
spec.define_item("Cone Ball", category="Traps", trap=True)
spec.define_item("Icosphere Ball", category="Traps", trap=True)
spec.define_item("Puck Ball", category="Traps", trap=True)
spec.define_item("Star Ball", category="Traps", trap=True)
spec.define_item("Acorn Ball", category="Traps", trap=True)
spec.define_item("Ornament Ball", category="Traps", trap=True)
spec.define_item("Chicken Nugget Ball", category="Traps", trap=True)

spec.define_item("Small Ball", category="Traps", trap=True, count=3)
spec.define_item("Large Ball", category="Traps", trap=True, count=3)

spec.define_item("Medium Bouncy Ground", category="Traps", trap=True)
spec.define_item("High Bouncy Ground", category="Traps", trap=True)
# endregion traps
