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

course_completion = spec.define_item(
    "Course Completion",
    category="Victory",
    count=len(courses),
    progression=True,
)

spec.define_location(
    "Win!",
    category="Victory",
    requires=Requires.item(course_completion, "50%"),
    victory=True,
)

course_progressive_item_count = 10

course_item_category = f"Courses ({course_progressive_item_count} Needed)"


def get_course_item_name(course: str) -> str:
    return f"{course} (Progressive Courses)"


for course in courses:
    course_item = spec.define_item(
        get_course_item_name(course),
        category=course_item_category,
        progression=True,
        count=course_progressive_item_count,
    )

    for hole in range(1, 18 + 1):
        course_hole_location = spec.define_location(
            f"{course} - Hole {hole}",
            category=f"Courses - {course}",
            requires=Requires.item(course_item, "all"),
        )
        if hole == 18:
            course_hole_location["place_item"] = [course_completion["name"]]

for i in range(1, 10 + 1):
    spec.define_location(
        f"Hole in One! (x{i})",
        category="Achievements",
        # don't want for-fun achievements to have important shit
        dont_place_item=["Max Time +10s"],
        dont_place_item_category=[course_item_category],
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
spec.define_item("Gravity 0.25", category="Traps (Gravity)", trap=True)
spec.define_item("Gravity 0.5", category="Traps (Gravity)", trap=True)
spec.define_item("Gravity 0.75", category="Traps (Gravity)", trap=True)
spec.define_item("Egg Ball", category="Traps (Ball Shape)", trap=True)
spec.define_item("Cube Ball", category="Traps (Ball Shape)", trap=True)
spec.define_item("Cylinder Ball", category="Traps (Ball Shape)", trap=True)
spec.define_item("Cone Ball", category="Traps (Ball Shape)", trap=True)
spec.define_item("Icosphere Ball", category="Traps (Ball Shape)", trap=True)
spec.define_item("Puck Ball", category="Traps (Ball Shape)", trap=True)
spec.define_item("Star Ball", category="Traps (Ball Shape)", trap=True)
spec.define_item("Acorn Ball", category="Traps (Ball Shape)", trap=True)
spec.define_item("Large Ball", category="Traps (Ball Size)", trap=True)
spec.define_item("Small Ball", category="Traps (Ball Size)", trap=True)
spec.define_item("Medium Bouncy Ground", category="Traps (Bouncy Ground)", trap=True)
spec.define_item("High Bouncy Ground", category="Traps (Bouncy Ground)", trap=True)
# endregion traps
