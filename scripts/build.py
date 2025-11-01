import argparse
from dataclasses import dataclass, field
from pathlib import Path

from .lib.log import PrettyLog

from .lib.multiworld import MultiWorldConfig
from .lib.manual_worlds import find_local_manual_world_projects


def __main():

    @dataclass
    class Args:
        worlds: list[str] = field(default_factory=list)
        multi: str | None = None

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "worlds",
        nargs="*",
        default=[],
        help="Name of worlds to build, e.g. `distance` refers to the world at `manual_worlds/distance`",
    )

    arg_parser.add_argument(
        "-m",
        "--multi",
        default=None,
        help=(
            "The name of a multiworld config to use,"
            + " e.g. specify `solosync` to use the config at `config/multiworlds/solosync.yaml`"
        ),
    )

    args = arg_parser.parse_args(namespace=Args())

    if args.worlds:
        all_worlds = [*find_local_manual_world_projects()]
        worlds_to_build = (
            [world for world in all_worlds if world.name in args.worlds] # fmt: skip
            or all_worlds
        )
    elif args.multi:
        multiworld_config = MultiWorldConfig.named(args.multi)
        PrettyLog.info(
            "Using multiworld config:", multiworld_config.path.relative_to(Path.cwd())
        )

        if not multiworld_config.player_configs:
            PrettyLog.error("No player configs found")
            exit(1)

        player_config_world_ids = {c.game for c in multiworld_config.player_configs}
        worlds_to_build = [
            manual_world_project
            for manual_world_project in find_local_manual_world_projects()
            if manual_world_project.world_id in player_config_world_ids
        ]
    else:
        PrettyLog.error("Expected 1+ worlds or a --multi (-m)\n")
        arg_parser.print_help()
        exit(1)

    for world in worlds_to_build:
        PrettyLog.working(f"Building {world.name}...")
        final_destination_fox_only_no_items = world.build()
        PrettyLog.done(f"Built at {final_destination_fox_only_no_items}")


if __name__ == "__main__":
    __main()
