import asyncio
from dataclasses import dataclass
from itertools import combinations
import json
import re
from typing import Final
import websockets
import websockets.asyncio
import websockets.asyncio.client


PARTICIPANT_WORLDS: Final = {
    "Hatsune Miku Project Diva Mega Mix+",
    "Manual_FortniteFestival_UnderseaRexieVT",
    "Manual_GrooveCoaster_claiomh",
    "Manual_HeavenStudio_Octomari",
    "Manual_ProjectAfternightSymphonyMix_Scrungip",
    "Manual_SoundVoltex_MapleLeaf",
    "Manual_TouhouDanmakuKaguraPhantasiaLost_MapleLeaf",
    "Manual_VibRibbon_Emik",
    "Muse Dash",
}


async def __main():
    @dataclass
    class SongItem:
        item_name: str
        game_name: str

        def __post_init__(self):
            self.song_name = self.item_name
            if "AsortedRhythm" in self.game_name or "GrooveCoaster" in self.game_name:
                self.song_name = (
                    self.item_name.replace("GC ", "")
                    .replace("RH ", "")
                    .replace("PH ", "")
                )
            if self.game_name == "Hatsune Miku Project Diva Mega Mix+":
                self.song_name = re.sub(r"\s\[\d+\]$", "", self.item_name)

    async with websockets.asyncio.client.connect(
        "ws://localhost:38281", max_size=2**32
    ) as socket:
        game_items: dict[str, dict[str, SongItem]] = {
            world: {} for world in PARTICIPANT_WORLDS
        }

        match json.loads(await socket.recv()):
            case [{"cmd": "RoomInfo", "games": [*included_games_list]}, *_]:
                # game_items = {game: {} for game in included_games_list}
                await socket.send(json.dumps([{"cmd": "GetDataPackage"}]))
            case received:
                raise Exception("Expected room info, got:", received)

        match json.loads(await socket.recv()):
            case [{"cmd": "DataPackage", "data": {"games": {**received_games}}}, *_]:
                for game in game_items:
                    game_items[game] = {
                        item_name: SongItem(item_name, game)
                        for item_name in received_games[game]["item_name_to_id"]
                    }
            case received:
                raise Exception("Expected data package, got:", received)

        await socket.close()

        links_by_song: dict[str, dict[str, str | bool]] = {
            # example:
            # "Bad Apple!! feat. nomico": {
            #     "Manual_SoundVoltex_MapleLeaf": "Bad Apple!! feat.nomico",
            #     "Hatsune Miku Project Diva Mega Mix+": "Bad Apple!! feat.nomico [4552]",
            # }
        }
        # existing_songs = set(i.lower() for i in LINKED_SONG_NAMES)

        for game_a, game_b in combinations(game_items, 2):
            for item_a in game_items[game_a].values():
                # if item_a.song_name.lower() in existing_songs:
                #     continue

                for item_b in game_items[game_b].values():
                    # if item_b.song_name.lower() in existing_songs:
                    #     continue

                    if item_a.song_name.lower() == item_b.song_name.lower():
                        song_links = links_by_song.setdefault(item_a.song_name, {})
                        song_links[game_a] = item_a.item_name
                        song_links[game_b] = item_b.item_name

        print(json.dumps(links_by_song, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(__main())
