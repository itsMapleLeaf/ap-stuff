import asyncio
from dataclasses import dataclass
import difflib
import json
import re
from typing import ClassVar, TypedDict
import websockets
import websockets.asyncio
import websockets.asyncio.client

from ._paths import project_dir


songlink_world_src = project_dir / "manual_worlds/symphony_songlink/src"


async def __generate_items():
    class LinkedSong:
        library: ClassVar

        def __init__(self, artist: str | list[str], title: str | list[str]) -> None:
            self.artist = _resolve_optional_list(artist)
            self.title = _resolve_optional_list(title)

    LinkedSong.library = [
        LinkedSong(
            title="Conflict",
            artist="siromaru & Cranky",
        ),
        LinkedSong(
            title="FREEDOM DiVE",
            artist="xi",
        ),
        LinkedSong(
            title="Mopemope",
            artist="LeaF",
        ),
        LinkedSong(
            title="GOODTEK",
            artist="EBIMAYO",
        ),
        LinkedSong(
            title="Brain Power",
            artist="Noma",
        ),
        LinkedSong(
            title=["Rolling Girl", "ローリンガール"],
            artist="wowaka",
        ),
        LinkedSong(
            title="Wavetapper",
            artist="Frums",
        ),
        LinkedSong(
            title="Verflucht",
            artist="Tyrfing",
        ),
        LinkedSong(
            title="BLACK or WHITE?",
            artist="BlackYooh vs. siromaru",
        ),
        LinkedSong(
            title="Chronomia",
            artist="Lime",
        ),
        LinkedSong(
            title="Miku",
            artist="Anamanaguchi",
        ),
        LinkedSong(
            title=["Bad Apple!! feat. nomico", "Bad Apple!!", "Bad Apple"],
            artist="Alstroemeria Records",
        ),
        LinkedSong(
            title="MEGALOVANIA",
            artist="Toby Fox",
        ),
        LinkedSong(
            title=["Knight of Nights", "ナイト・オブ・ナイツ"],
            artist=["beatMARIO (COOL&CREATE)", "ビートまりお"],
        ),
        LinkedSong(
            title=["Roki", "ロキ"],
            artist=["mikitoP", "みきとP"],
        ),
        LinkedSong(
            title=["Senbonzakura", "千本桜"],
            artist=["KurousaP", "黒うさP"],
        ),
        LinkedSong(
            title="ECHO",
            artist="CIRCRUSH",
        ),
        LinkedSong(
            title="Never Gonna Give You Up",
            artist="Various Artists",
        ),
        LinkedSong(
            title="GANGNAM STYLE",
            artist="PSY",
        ),
    ]

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

    class DataPackageGame(TypedDict):
        item_name_to_id: dict[str, int]

    async with websockets.asyncio.client.connect(
        "ws://localhost:38281", max_size=2**32
    ) as socket:
        print("open")

        async def handle_messages():
            connected = True
            games_in_multi: set[str] = set()

            while connected:
                message_string = await socket.recv()
                commands = json.loads(message_string)

                for command in commands:
                    match command:
                        case {"cmd": "RoomInfo", "games": [*received_games_in_multi]}:
                            print("received games:", received_games_in_multi)
                            games_in_multi = set(received_games_in_multi)
                            await socket.send(json.dumps([{"cmd": "GetDataPackage"}]))
                        case {
                            "cmd": "DataPackage",
                            "data": {"games": {**received_games}},
                        }:
                            print("got data package")

                            received_games: dict[str, DataPackageGame]

                            game_items = {
                                game: {
                                    item_name: SongItem(item_name, game)
                                    for item_name in game_data["item_name_to_id"].keys()
                                }
                                for game, game_data in received_games.items()
                                if game in games_in_multi
                            }

                            print("closing socket")

                            await socket.close()

                            return game_items
                        case _:
                            print("unknown message", message_string[:1000])

            raise Exception("Failed to get game items")

        game_items = await asyncio.wait_for(handle_messages(), timeout=3)
        print("socket closed")

    items = []

    for song in LinkedSong.library:
        song_item_name = f"{song.title[0]} (by {song.artist[0]})"
        song_item_links: dict[str, list[str]] = {}

        for game_name, game_songs in game_items.items():
            for song_title_entry in song.title:
                [(matched_song_item, matched_ratio), *_] = sorted(
                    (
                        (
                            song_item,
                            difflib.SequenceMatcher(
                                None,
                                song_item.song_name.lower(),
                                song_title_entry.lower(),
                            ).ratio(),
                        )
                        for song_item in game_songs.values()
                    ),
                    key=lambda item: item[1],
                    reverse=True,
                )

                if matched_ratio > 0.8:
                    song_item_links.setdefault(game_name, []).append(
                        matched_song_item.item_name
                    )
                    break

        items.append(
            {
                "name": song_item_name,
                "progression": True,
                "count": 10,
                "linklink": song_item_links,
            }
        )

    return items


async def __main() -> None:
    items = __generate_items()

    with open(
        songlink_world_src / "data/items.json", mode="w", encoding="utf8"
    ) as items_file:
        json.dump(items, items_file, indent=4, ensure_ascii=False)


def _resolve_optional_list[T](value: T | list[T]) -> list[T]:
    return value if isinstance(value, list) else [value]


if __name__ == "__main__":
    asyncio.run(__main())
