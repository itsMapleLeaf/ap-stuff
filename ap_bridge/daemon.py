import argparse
import asyncio
from dataclasses import dataclass
import json
import sys
from typing import Final
from worlds.AutoWorld import AutoWorldRegister
from worlds import LauncherComponents
from worlds.tracker.TrackerClient import TrackerGameContext


class DaemonComponent(LauncherComponents.Component):
    __name: Final = "AP Bridge - Daemon"

    def __init__(self) -> None:
        super().__init__(
            self.__name,
            func=lambda: asyncio.run(self.__main()),
            cli=True,
            description="Starts the daemon background process for AP Bridge",
        )

    async def __main(self, *cli_args: str) -> None:
        # parser = argparse.ArgumentParser(
        #     self.__name,
        #     usage=f"{sys.executable} {self.__name}",
        # )

        # parser.add_argument(
        #     "world",
        #     help="The name of the world, e.g. 'Manual_SoundVoltex_MapleLeaf'",
        # )

        # @dataclass(init=False)
        # class InspectManualArgs:
        #     world: str

        # args = parser.parse_args(cli_args, InspectManualArgs())

        trackers = dict[str, TrackerGameContext]()

        def print_err(*messages: object):
            print(*messages, file=sys.stderr)

        while True:
            command_input = await asyncio.get_event_loop().run_in_executor(None, input)

            try:
                command: object = json.loads(command_input)
            except json.JSONDecodeError as ex:
                print_err(ex.msg)
                continue

            match command:
                case {
                    "type": "start_tracker",
                    "address": str(address),
                    "password": str(password),
                    "name": str(slot_name),
                    "game": str(world_name),
                }:
                    tag = f"{address}|{slot_name}"
                    trackers[tag] = self.__start_tracker(
                        address, password, slot_name, world_name
                    )

                case {
                    "type": "stop_tracker",
                    "address": str(address),
                    "name": str(slot_name),
                }:
                    tag = f"{address}|{slot_name}"
                    await trackers[tag].disconnect()
                    trackers.pop(tag)

                case _:
                    print_err("Unrecognized command:", command)

    def __start_tracker(
        self, address: str, password: str, slot_name: str, world_name: str
    ):
        def handle_update(locations: list[str]):
            print(
                json.dumps(
                    {
                        "type": "tracker_update",
                        "address": address,
                        "password": password,
                        "locations": locations,
                    }
                )
            )
            return True

        def handle_events_update(events: list[str]):
            print(
                json.dumps(
                    {
                        "type": "tracker_events_update",
                        "address": address,
                        "password": password,
                        "events": events,
                    }
                )
            )
            return True

        context = TrackerGameContext(address, password)

        context.auth = slot_name
        context.game = world_name

        context.set_callback(handle_update)
        context.set_events_callback(handle_events_update)

        return context
