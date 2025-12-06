import argparse
from dataclasses import dataclass
import json
import sys
from typing import Final
from worlds.AutoWorld import AutoWorldRegister
from worlds import LauncherComponents


class InspectManualComponent(LauncherComponents.Component):
    __name: Final = "AP Bridge - Inspect Manual"

    def __init__(self) -> None:
        super().__init__(self.__name, func=self.__main, cli=True)

    def __main(self, *cli_args: str) -> None:
        parser = argparse.ArgumentParser(
            "Inspect Manual",
            description="Inspect and output the data for a manual world",
            usage=f"{sys.executable} {self.__name} -- <world>",
        )

        parser.add_argument(
            "world",
            help="The name of the world, e.g. 'Manual_SoundVoltex_MapleLeaf'",
        )

        @dataclass(init=False)
        class InspectManualArgs:
            world: str

        args = parser.parse_args(cli_args, InspectManualArgs())

        if not (world_type := AutoWorldRegister.world_types.get(args.world, None)):
            available_worlds = sorted(
                AutoWorldRegister.world_types.keys(), key=lambda str: str.lower()
            )

            print(f"World '{args.world}' does not exist. Available worlds:")
            for world_key in available_worlds:
                print(f"- {world_key}")

        manual_data = {
            "locations": getattr(world_type, "location_table", []),
            "items": getattr(world_type, "item_table", []),
            "categories": getattr(world_type, "category_table", {}),
        }

        json.dump(manual_data, fp=sys.stdout)
        print("", flush=True)


LauncherComponents.components.append(InspectManualComponent())
