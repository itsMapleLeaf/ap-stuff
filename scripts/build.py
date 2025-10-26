import sys
from .lib.manual_worlds import find_local_manual_world_projects


def __main():
    all_worlds = [*find_local_manual_world_projects()]

    world_args = set(sys.argv[1:])
    worlds_to_build = (
        [world for world in all_worlds if world.name in world_args] # fmt: skip
        or all_worlds
    )

    for world in worlds_to_build:
        print(f"Building {world.name}...")
        final_destination_fox_only_no_items = world.build()
        print(f"Built at {final_destination_fox_only_no_items}")


if __name__ == "__main__":
    __main()
