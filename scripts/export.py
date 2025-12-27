import os
import shutil
import sys
from showinfm.showinfm import show_in_file_manager
import yaml

from .lib.multiworld import MultiWorldConfig
from .lib.paths import project_dir, user_archipelago_worlds_dir


def __main():
    multiworld_arg = sys.argv[1]
    multiworld_config = MultiWorldConfig.named(multiworld_arg)

    output_dir = project_dir / "dist/export" / multiworld_arg
    combined_player_config_file_name = (
        "+".join(config.path.stem for config in multiworld_config.player_configs)
        + ".yaml"
    )
    combined_config_path = output_dir / combined_player_config_file_name

    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir)

    with open(combined_config_path, "w", encoding="utf8") as combined_config_file:
        yaml.dump_all(
            [config.data for config in multiworld_config.player_configs],
            combined_config_file,
            sort_keys=False,
            allow_unicode=True,
        )

    included_worlds = {
        user_archipelago_worlds_dir
        / f"{str(config.game).replace('Manual','manual',1)}.apworld"
        for config in multiworld_config.player_configs
        if "Manual" in str(config.game)
    }

    for world_path in included_worlds:
        shutil.copy(world_path, output_dir)

    show_in_file_manager(str(output_dir))


if __name__ == "__main__":
    __main()
