import asyncio
import json
from pprint import pp
from typing import TypedDict
import websockets
import websockets.asyncio
import websockets.asyncio.client


linked_songs = {
    "Conflict": {
        "Manual_GrooveCoaster_claiomh": "GC Conflict",
        "Manual_SoundVoltex_dev_MapleLeaf": "conflict",
        "Muse Dash": "conflict",
    },
    "FREEDOM DiVE": {
        "Manual_SoundVoltex_dev_MapleLeaf": "FREEDOM DiVE",
        "Muse Dash": "FREEDOM DiVE",
    },
    "GOODTEK": {
        "Manual_SoundVoltex_dev_MapleLeaf": "GOODTEK",
        "Muse Dash": "GOODTEK",
    },
    "Brain Power": {
        "Manual_GrooveCoaster_claiomh": "GC Brain Power",
        "Muse Dash": "Brain Power",
    },
    "Rolling Girl": {
        "Manual_SoundVoltex_dev_MapleLeaf": "ローリンガール",
        "Manual_ProjectAfternightSymphonyMix_Scrungip": "Rolling Girl",
        "Hatsune Miku Project Diva Mega Mix+": "Rolling Girl",
    },
    "Chronomia": {
        "Manual_SoundVoltex_dev_MapleLeaf": "Chronomia",
        "Muse Dash": "Chronomia",
    },
    "Miku": {
        "Manual_FortniteFestival_UnderseaRexieVT": "Miku",
        "Hatsune Miku Project Diva Mega Mix+": "Miku [9165]",
    },
    "Bad Apple!! feat. nomico": {
        "Manual_SoundVoltex_dev_MapleLeaf": "Bad Apple!! feat. nomico",
        "Manual_TouhouDanmakuKaguraPhantasiaLost_MapleLeaf": "Bad Apple!! feat.nomico",
        "Hatsune Miku Project Diva Mega Mix+": "Bad Apple!! feat.nomico [4552]",
        "Muse Dash": "Bad Apple!! feat. Nomico",
    },
    "MEGALOVANIA": {
        "Manual_GrooveCoaster_claiomh": "GC megolavania",
        "Manual_SoundVoltex_dev_MapleLeaf": "MEGALOVANIA",
        "Manual_ProjectAfternightSymphonyMix_Scrungip": "MEGALOVANIA",
    },
    "Knight of Nights": {
        "Manual_GrooveCoaster_claiomh": "GC Night of Knights",
        "Manual_SoundVoltex_dev_MapleLeaf": "ナイト・オブ・ナイツ",
        "Manual_TouhouDanmakuKaguraPhantasiaLost_MapleLeaf": "Knight of Nights",
        "Hatsune Miku Project Diva Mega Mix+": "Knight of Light",
        "Muse Dash": "Night of Nights",
    },
    "Roki": {
        "Manual_GrooveCoaster_claiomh": "GC Roki",
        "Manual_SoundVoltex_dev_MapleLeaf": "ロキ",
        "Hatsune Miku Project Diva Mega Mix+": "ROKI",
    },
    "Senbonzakura": {
        "Manual_SoundVoltex_dev_MapleLeaf": "千本桜",
        "Hatsune Miku Project Diva Mega Mix+": "Senbonzakura",
    },
    "ECHO": {
        "Manual_GrooveCoaster_claiomh": "GC Echo",
        "Manual_SoundVoltex_dev_MapleLeaf": "ECHO",
        "Manual_ProjectAfternightSymphonyMix_Scrungip": "ECHO",
        "Hatsune Miku Project Diva Mega Mix+": "ECHO [950]",
    },
    "Never Gonna Give You Up": {
        "Manual_FortniteFestival_UnderseaRexieVT": "Never Gonna Give You Up",
        "Hatsune Miku Project Diva Mega Mix+": "Never Gonna Give You Up [4528]",
    },
    "GANGNAM STYLE": {
        "Manual_FortniteFestival_UnderseaRexieVT": "Gangnam Style",
        "Manual_ProjectAfternightSymphonyMix_Scrungip": "Gangnam Style",
        "Hatsune Miku Project Diva Mega Mix+": "GANGNAM STYLE [3399]",
    },
}


async def __main():
    class DataPackageGame(TypedDict):
        item_name_to_id: dict[str, int]

    async with websockets.asyncio.client.connect(
        "ws://localhost:38281", max_size=2**32
    ) as socket:
        print("open")

        connected = True

        while connected:
            message_string = await socket.recv()
            commands = json.loads(message_string)

            for command in commands:
                match command:
                    case {"cmd": "RoomInfo", **data}:
                        pp(data)
                        # await socket.send(json.dumps([{"cmd": "GetDataPackage"}]))
                        await socket.send(
                            json.dumps(
                                [
                                    {
                                        "cmd": "Connect",
                                        "game": "Manual_SoundVoltex_dev_MapleLeaf",
                                        "name": "MapleVoltex",
                                        "password": None,
                                        "uuid": "",
                                        "version": {
                                            "class": "Version",
                                            "major": 0,
                                            "minor": 6,
                                            "build": 0,
                                        },
                                        "items_handling": 0b011,
                                        "tags": [],
                                        "slot_data": False,
                                    }
                                ]
                            )
                        )
                    case {"cmd": "DataPackage", "data": {"games": {**received_games}}}:
                        print("got data package")
                    case {"cmd": "Connected"}:
                        await socket.send(
                            json.dumps(
                                [
                                    {
                                        "cmd": "Say",
                                        "text": "!admin login pbKGehi626cz6C",
                                    }
                                ]
                            )
                        )
                        await asyncio.sleep(0.1)
                        await socket.send(
                            json.dumps(
                                [
                                    {
                                        "cmd": "Say",
                                        "text": "!remaining",
                                    }
                                ]
                            )
                        )
                    case _:
                        print("unknown message", message_string[:1000])


if __name__ == "__main__":
    asyncio.run(__main())
