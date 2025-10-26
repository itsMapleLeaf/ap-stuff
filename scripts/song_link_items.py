import asyncio
import json
from typing import Final

from .paths import project_dir

LINKED_SONG_NAMES: Final = [
    "B.B.K.K.B.K.K.",
    "Bad Apple!! feat. nomico",
    "BLACK or WHITE?",
    "Brain Power",
    "Chronomia",
    "Conflict",
    "ECHO",
    "FREEDOM DiVE",
    "GANGNAM STYLE",
    "GOODTEK",
    "Knight of Nights",
    "MEGALOVANIA",
    "Miku",
    "Mopemope",
    "Never Gonna Give You Up",
    "Roki",
    "Rolling Girl",
    "Senbonzakura",
    "Verflucht",
]

# The linked songs for each world,
# where each world maps to a dict of the linked song name to the item name in the world,
# or `True` if the item name is the same as the linked song name.
LINKS_BY_WORLD: Final[dict[str, dict[str, str]]] = {
    "Manual_SoundVoltex_MapleLeaf": {
        "B.B.K.K.B.K.K.": "B.B.K.K.B.K.K.",
        "Bad Apple!! feat. nomico": "Bad Apple!! feat. nomico",
        "BLACK or WHITE?": "BLACK or WHITE?",
        "Chronomia": "Chronomia",
        "Conflict": "conflict",
        "ECHO": "ECHO",
        "FREEDOM DiVE": "FREEDOM DiVE",
        "GOODTEK": "GOODTEK",
        "Knight of Nights": "ナイト・オブ・ナイツ",
        "MEGALOVANIA": "MEGALOVANIA",
        "Roki": "ロキ",
        "Rolling Girl": "ローリンガール",
        "Senbonzakura": "千本桜",
        "Verflucht": "Verflucht",
    },
    "Manual_GrooveCoaster_claiomh": {
        "B.B.K.K.B.K.K.": "GC B.B.K.K.B.K.K.",
        "Bad Apple!! feat. nomico": "GC Bad Apple",
        "Brain Power": "GC Brain Power",
        "Conflict": "GC Conflict",
        "ECHO": "GC Echo",
        "Knight of Nights": "GC Night of Knights",
        "MEGALOVANIA": "GC megolavania",
        "Roki": "GC Roki",
    },
    "Manual_VibRibbon_Emik": {
        "B.B.K.K.B.K.K.": "B.B.K.K.B.K.K.",
        "Bad Apple!! feat. nomico": "Bad Apple!! feat. nomico",
        "BLACK or WHITE?": "BLACK or WHITE?",
        "Brain Power": "Brain Power",
        "Chronomia": "Chronomia",
        "Conflict": "Conflict",
        "ECHO": "ECHO",
        "FREEDOM DiVE": "FREEDOM DiVE",
        "GOODTEK": "GOODTEK",
        "Knight of Nights": "Knight of Nights",
        "MEGALOVANIA": "Megalovania",
        "Miku": "Miku",
        "Mopemope": "MopeMope",
        "Never Gonna Give You Up": "Never Gonna Give You Up",
        "Roki": "Roki / ロキ",
        "Rolling Girl": "Rolling Girl / ローリンガール",
        "Senbonzakura": "Senbonzakura / 千本桜",
        "Verflucht": "Verflucht",
    },
    "Manual_TouhouDanmakuKaguraPhantasiaLost_MapleLeaf": {
        "Bad Apple!! feat. nomico": "Bad Apple!! feat.nomico",
        "Knight of Nights": "Knight of Nights",
    },
    "Hatsune Miku Project Diva Mega Mix+": {
        "Bad Apple!! feat. nomico": "Bad Apple!! feat.nomico [4552]",
        "ECHO": "ECHO [950]",
        "GANGNAM STYLE": "GANGNAM STYLE [3399]",
        "Miku": "Miku [9165]",
        "Never Gonna Give You Up": "Never Gonna Give You Up [4528]",
        "Roki": "ROKI",
        "Rolling Girl": "Rolling Girl",
        "Senbonzakura": "Senbonzakura",
    },
    "Muse Dash": {
        "Bad Apple!! feat. nomico": "Bad Apple!! feat. Nomico",
        "Brain Power": "Brain Power",
        "Chronomia": "Chronomia",
        "Conflict": "conflict",
        "FREEDOM DiVE": "FREEDOM DiVE",
        "GOODTEK": "GOODTEK",
        "Knight of Nights": "Night of Nights",
        "Mopemope": "Mopemope",
    },
    "Manual_ProjectAfternightSymphonyMix_Scrungip": {
        "ECHO": "ECHO",
        "GANGNAM STYLE": "Gangnam Style",
        "MEGALOVANIA": "MEGALOVANIA",
        "Rolling Girl": "Rolling Girl",
    },
    "Manual_HeavenStudio_Octomari": {
        "ECHO": "ECHO (lotusdom)",
        "FREEDOM DiVE": "widget dive (lifinale)",
    },
    "Manual_FortniteFestival_UnderseaRexieVT": {
        "GANGNAM STYLE": "Gangnam Style",
        "Miku": "Miku",
        "Never Gonna Give You Up": "Never Gonna Give You Up",
    },
}


async def __main() -> None:
    items = [
        {
            "name": song_name,
            "progression": True,
            "count": 1,
            "linklink": {
                world: [links[song_name] == True and song_name or links[song_name]]
                for world, links in LINKS_BY_WORLD.items()
                if song_name in links
            },
        }
        for song_name in LINKED_SONG_NAMES
    ]

    with open(
        project_dir / "manual_worlds/symphony_songlink/src" / "data/items.json",
        mode="w",
        encoding="utf8",
    ) as items_file:
        json.dump(items, items_file, indent="\t", ensure_ascii=False)


if __name__ == "__main__":
    asyncio.run(__main())
