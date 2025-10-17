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
    category="Upgrades - Settings",
    useful=True,
    count=24,
    early=3,
    starting_count=3,
)

spec.define_item(
    "Max Shots +1",
    category="Upgrades - Settings",
    useful=True,
    count=15,
    early=3,
    starting_count=6,
)

spec.define_item(
    "Free-cam Time +2s",
    category="Upgrades - Abilities",
    useful=True,
    count=15,
)


def __define_ability(name: str, count: int = 2) -> None:
    spec.define_item(name, category="Upgrades - Abilities", useful=True, count=count)


__define_ability("Retry Shot")
__define_ability("Ball Spin")
__define_ability("Jumping")
__define_ability("Spiking")
__define_ability("Handbrake")
__define_ability("Show Last Power")
# endregion upgrades

# region traps
spec.define_item(
    "Cancel Trap",
    category="Cancel Trap (One-time use, clear all traps in one category)",
    useful=True,
    count=10,
)


def __define_gravity_trap(name: str, count: int = 3) -> None:
    spec.define_item(
        name,
        category="Traps - Gravity (Apply Latest)",
        trap=True,
        count=count,
    )


__define_gravity_trap("Gravity 0.25")
__define_gravity_trap("Gravity 0.50")
__define_gravity_trap("Gravity 0.75")


def __define_shape_trap(name: str) -> None:
    spec.define_item(
        name,
        category="Traps - Ball Shape (Apply Latest)",
        trap=True,
    )


__define_shape_trap("Egg")
__define_shape_trap("Cube")
__define_shape_trap("Cylinder")
__define_shape_trap("Cone")
__define_shape_trap("Icosphere")
__define_shape_trap("Puck")
__define_shape_trap("Star")
__define_shape_trap("Acorn")
__define_shape_trap("Bauble")
__define_shape_trap("Random Shape - Each")
__define_shape_trap("Random Shape - All")


def __define_size_trap(name: str, count: int = 3) -> None:
    spec.define_item(
        name,
        category="Traps - Ball Size (Apply Latest)",
        trap=True,
        count=count,
    )


__define_size_trap("Small Ball")
__define_size_trap("Large Ball")
__define_size_trap("Random Size - Each")
__define_size_trap("Random Size - All")


def __define_bouncy_ground_trap(name: str, count: int = 2) -> None:
    spec.define_item(
        name,
        category="Traps - Bouncy Ground (Apply Latest)",
        trap=True,
        count=count,
    )


__define_bouncy_ground_trap("Medium Bouncy Ground")
__define_bouncy_ground_trap("High Bouncy Ground")
# endregion traps
