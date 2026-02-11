import asyncio
from collections import defaultdict
from dataclasses import dataclass
import itertools
import json
from pathlib import Path
from pprint import pprint
from typing import Any, Literal, NotRequired, TypedDict
import requests
import pyquery

SONG_TITLE_JP = "曲名"
ARTIST_JP = "アーティスト"

SONGS_FILE_PATH = (
    Path(__file__).parent.parent.parent / "manual_worlds/sdvx/data/songs.json"
)

PAGES = [
    # new songs
    {
        "type": "default",
        "url": "https://bemaniwiki.com/?SOUND+VOLTEX+%A2%E0/%BF%B7%B6%CA%A5%EA%A5%B9%A5%C8",
    },
    # old songs (booth ~ gravity wars)
    {
        "type": "default",
        "url": "https://bemaniwiki.com/?SOUND+VOLTEX+%A2%E0/%B5%EC%B6%CA%A5%EA%A5%B9%A5%C8%28BOOTH%A1%C1III+GRAVITY+WARS%29",
    },
    # old songs (heavenly haven ~ exceed gear)
    {
        "type": "default",
        "url": "https://bemaniwiki.com/?SOUND+VOLTEX+%A2%E0/%B5%EC%B6%CA%A5%EA%A5%B9%A5%C8%28IV+HEAVENLY+HAVEN%A1%C1EXCEED+GEAR%29",
    },
    # blaster gate
    {
        "type": "blaster_gate",
        "url": "https://bemaniwiki.com/?SOUND+VOLTEX+%A2%E0/BLASTER+GATE",
    },
    # variant gate
    {
        "type": "variant_gate",
        "url": "https://bemaniwiki.com/?SOUND+VOLTEX+%A2%E0/VARIANT+GATE",
    },
]


class SongData(TypedDict):
    # title: str
    artist: NotRequired[str]
    nov: NotRequired[float]
    adv: NotRequired[float]
    exh: NotRequired[float]
    mxm: NotRequired[float]


async def main():
    tasks: list[asyncio.Task[str]] = []

    for page in PAGES:
        thread_coro = asyncio.to_thread(fetch_text, page["url"])
        tasks.append(asyncio.create_task(thread_coro))

    songs: dict[str, SongData] = {}

    for content in await asyncio.gather(*tasks):
        pq = pyquery.PyQuery(content)

        tables = [*pq("table").items()]
        print(f"found {len(tables)} tables")

        for table in tables:
            # the table is full of rowspans which make "holes" in each row;
            # we can't just assume the index of a td in the row is the actual column index
            # so for simplicity's sake, first convert the table into a flat 2D matrix,
            # where cells get "extended" in the matrix across their spans
            table_head_dict = parse_table_matrix(table("thead"))
            table_body_dict = parse_table_matrix(table("tbody"))

            def try_set_diff(
                song_name: str,
                diff_name: Literal["nov", "adv", "exh", "mxm"],
                diff_value: str,
            ):
                diff_value = "".join(c for c in diff_value if c.isdigit() or c == ".")
                if not diff_value:
                    return

                song = songs.setdefault(song_name, {})
                song[diff_name] = float(diff_value)

            match table_head_dict:
                case [
                    [
                        _,
                        "曲名",
                        "アーティスト",
                        "BPM",
                        "NOV",
                        "ADV",
                        "EXH",
                        ("MXM" | "INF" | "GRV" | "HVN" | "XCD"),
                        *_,
                    ],
                    *_,
                ]:
                    for song_row in table_body_dict:
                        title = song_row[1]
                        try_set_diff(title, "nov", song_row[4])
                        try_set_diff(title, "adv", song_row[5])
                        try_set_diff(title, "exh", song_row[6])
                        try_set_diff(title, "mxm", song_row[7])

                case [_, [_, "曲名", "NOV", "ADV", "EXH", "MXM", *_], *_]:
                    for song_row in table_body_dict:
                        title = song_row[1]
                        try_set_diff(title, "nov", song_row[2])
                        try_set_diff(title, "adv", song_row[3])
                        try_set_diff(title, "exh", song_row[4])
                        try_set_diff(title, "mxm", song_row[5])

                case [
                    [_, _, _, "アーティスト", "BPM", "NOV", "ADV", "EXH", "MXM"],
                    *_,
                ]:
                    for song_row in table_body_dict:
                        title = song_row[3]
                        try_set_diff(title, "nov", song_row[5])
                        try_set_diff(title, "adv", song_row[6])
                        try_set_diff(title, "exh", song_row[7])
                        try_set_diff(title, "mxm", song_row[8])

                case [
                    [_, "曲名", "アーティスト", "BPM", "NOV", "ADV", "EXH", *_],
                    *_,
                ]:
                    for song_row in table_body_dict:
                        title = song_row[1]
                        try_set_diff(title, "nov", song_row[4])
                        try_set_diff(title, "adv", song_row[5])
                        try_set_diff(title, "exh", song_row[6])

                case [[_, "曲名", "Lv", *_], *_]:
                    for song_row in table_body_dict:
                        title = song_row[1]
                        mxm = song_row[2]
                        try_set_diff(title, "mxm", mxm)

                case [[_, _, "曲名", "難易度", "Lv"], *_]:
                    for song_row in table_body_dict:
                        title = song_row[2]
                        try_set_diff(title, "mxm", song_row[4])

                case _:
                    print(f"skipping unrecognized table (headers: {table_head_dict})")
                    continue

    songs_list = [{**data, "title": title} for title, data in songs.items()]

    print(f"found {len(songs_list)} songs")

    with open(SONGS_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(
            songs_list,
            f,
            ensure_ascii=False,
            # use compact separators; we're not trying to be human-readable
            separators=(",", ":"),
        )


def fetch_text(url: str):
    print(f"fetching {url}")
    with requests.get(url) as r:
        return r.text


def parse_table_matrix(table_head_or_body: pyquery.PyQuery) -> list[list[str]]:
    matrix_dict = defaultdict(lambda: defaultdict(lambda: ""))

    for row_index, row in enumerate(table_head_or_body("tr").items()):
        cells = [*row("td").items()]
        # if the row just has one td in it, it's a section row and not a song; skip it
        if len(cells) == 1:
            # print(f'skipping presumed section row "{cells[0].text()}"')
            continue

        for col_index, cell in enumerate(cells):
            cell("a").remove()  # remove footnotes
            cell_content = str(cell.text()).replace("\n", " ").strip()
            cell_rowspan = int(cell.attr("rowspan") or 1)  # type: ignore
            cell_colspan = int(cell.attr("colspan") or 1)  # type: ignore

            # print(f"{cell_content=}")
            # print(f"{cell_rowspan=}")
            # print(f"{cell_colspan=}")

            matrix_row_start = row_index
            matrix_col_start = col_index

            # skip this col while there's already an existing one set in the matrix
            # from a prior row or col span
            while (
                matrix_row_start in matrix_dict
                and matrix_col_start in matrix_dict[matrix_row_start]
            ):
                matrix_col_start += 1

            # print(f"{matrix_row_start=}")
            # print(f"{matrix_col_start=}")

            for matrix_row in range(matrix_row_start, matrix_row_start + cell_rowspan):
                for matrix_col in range(
                    matrix_col_start, matrix_col_start + cell_colspan
                ):
                    matrix_dict[matrix_row][matrix_col] = cell_content.strip()

    # convert the defaultdict to a 2d list
    return [
        [matrix_dict[row_index][col_index] for col_index in sorted(row.keys())]
        for row_index, row in matrix_dict.items()
    ]


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
