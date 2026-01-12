import argparse
from dataclasses import dataclass, field
import glob
import os
from pathlib import Path
import shutil
import subprocess
from typing import Iterable

from .lib.paths import dist_dir, project_dir, user_archipelago_templates_dir
from .lib.log import PrettyLog
from .lib.multiworld import MultiWorldConfig
from .lib.manual_worlds import ManualWorldProject, find_local_manual_world_projects


def __cli():

    @dataclass
    class Args:
        worlds: list[str] = field(default_factory=list)
        multi: str | None = None
        all: bool = False
        release: bool = False

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

    arg_parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Build all local manual world projects",
    )

    arg_parser.add_argument(
        "-r",
        "--release",
        action="store_true",
        help="Create a GitHub release",
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
    elif args.all:
        worlds_to_build = [*find_local_manual_world_projects()]
    else:
        PrettyLog.error("Expected 1+ worlds, a --multi (-m)\n, or --all")
        arg_parser.print_help()
        exit(1)

    if args.release and len(worlds_to_build) != 1:
        PrettyLog.error("Can only use --release with a single world")
        exit(1)

    dist_build_dir = dist_dir / "build"

    try:
        shutil.rmtree(dist_build_dir)
    except FileNotFoundError:
        pass

    os.makedirs(dist_build_dir)

    for world in worlds_to_build:
        PrettyLog.working(f"Building {world.name}...")
        final_destination_fox_only_no_items = world.build()
        PrettyLog.done(f"Built at {final_destination_fox_only_no_items}")

        shutil.copy(
            final_destination_fox_only_no_items,
            dist_build_dir,
        )
        shutil.copy(
            user_archipelago_templates_dir / (world.world_id + ".yaml"),
            dist_build_dir,
        )

    if args.release:
        from scripts.gen_yamls import generate_yaml_templates

        generate_yaml_templates(
            target_folder=user_archipelago_templates_dir,
        )

        [world] = worlds_to_build
        subprocess.run(
            [
                *("gh", "release", "create"),
                f"{world.name}_v{world.version}",
                *glob.iglob("./dist/build/*", root_dir=project_dir),
                *("--title", f"{world.display_name} v{world.version}"),
                "--draft",
            ]
        )


if __name__ == "__main__":
    __cli()
