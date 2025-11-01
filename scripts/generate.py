import argparse
from dataclasses import dataclass
import glob
import os
import shutil
from zipfile import ZipFile

from .lib.multiworld import MultiWorldConfig
from .lib.args_override import ArgsOverride
from .lib.paths import dist_generate_dir, dist_generate_players_dir, project_dir


def __main():
    @dataclass(init=False)
    class Args:
        game_name: str

    parser = argparse.ArgumentParser()
    parser.add_argument("game_name")

    args = parser.parse_args(None, Args())

    multiworld_config = MultiWorldConfig.named(args.game_name)

    print(
        f'⚙️  Generating for "{args.game_name}"'
        f" ({multiworld_config.path.relative_to(project_dir)})"
    )

    if not multiworld_config.player_configs:
        print("⚠️ No player configs found")
        exit(1)

    output_dir = dist_generate_dir

    print(f"⚙️  Cleaning up output path")
    shutil.rmtree(output_dir)

    print(f"⚙️  Copying {len(multiworld_config.player_configs)} player configs")
    os.makedirs(dist_generate_players_dir)
    for player_config in multiworld_config.player_configs:
        shutil.copy(player_config.path, dist_generate_players_dir)

    print(f"⚙️  Running generator")

    # the generator isn't made to be invoked from a python script,
    # and the cleanest, most future-proof way to invoke it
    # is to override args so it parses them as if it were run via CLI
    #
    # gross, but better than subprocess!
    with ArgsOverride(
        # fmt: off
        "--player_files_path", dist_generate_players_dir,
        "--outputpath", output_dir,
        # fmt: on
    ):
        import Generate, Main

        (generator_args, generator_seed) = Generate.main()
        Main.main(generator_args, generator_seed)

    print(f"⚙️  Extracting files")

    generated_output_path = next(glob.iglob("AP_*.zip", root_dir=output_dir))
    with ZipFile(output_dir / generated_output_path) as generated_output_file:
        generated_output_file.extractall(output_dir)

    print(f"✅  Done")


if __name__ == "__main__":
    __main()
