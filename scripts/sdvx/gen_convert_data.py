from argparse import ArgumentParser
from dataclasses import dataclass
import dataclasses
import enum
import glob
import itertools
import json
import logging
import os
from pathlib import Path
import sys
from typing import Any, Literal, TypedDict
import difflib

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO").upper())


@dataclass
class Args:
    songs_folder: Path
    output_file: Path


arg_parser = ArgumentParser()
arg_parser.add_argument("songs_folder", type=Path)
arg_parser.add_argument(
    "-f",
    "--output-file",
    type=Path,
    default=Path("manual_worlds/sdvx/data/converts.json"),
)

logging.debug(f"{sys.argv=}")
args = Args(**vars(arg_parser.parse_args()))

# a map of song titles to the set of difficulties available
local_difficulties: dict[str, set[str]] = {}

ksm_difficulty_to_sdvx = {
    "light": "NOV",
    "challenge": "ADV",
    "extended": "EXH",
    "infinite": "MXM",
}

chart_entries = glob.glob("**/*.ksh", root_dir=args.songs_folder, recursive=True)
chart_entry_count = len(chart_entries)
logging.info(f"Found {chart_entry_count} charts")

for index, chart_entry in enumerate(chart_entries):
    try:
        chart_path = Path(args.songs_folder) / chart_entry
        chart_file_content = chart_path.read_text(encoding="utf-8-sig", errors="ignore")

        chart_data = {}

        for line in chart_file_content.splitlines():
            if line == "--":
                break
            if not line.strip():
                continue
            try:
                [key, value] = line.split("=", 1)
                chart_data[key] = value
            except ValueError as e:
                logging.error(f"Failed to parse line in {chart_entry}: {line!r}")
                continue

        chart_title = chart_data.get("title", "").strip()
        if not chart_title:
            logging.error(f"No title found in {chart_entry}")
            continue

        chart_difficulties = local_difficulties.setdefault(chart_title, set())
        chart_difficulties.add(
            ksm_difficulty_to_sdvx.get(chart_data["difficulty"], "NOV")
        )
    except Exception as e:
        logging.error(f"Failed to process {chart_entry}", e)

    if (index + 1) % 100 == 0:
        logging.info(f"Processed {index+1}/{chart_entry_count} charts")

official_song_groups: dict[str, list[dict[str, Any]]] = json.loads(
    Path("manual_worlds/sdvx/data/songs.json").read_text(
        encoding="utf-8", errors="ignore"
    )
)
official_song_titles = set[str](
    song["title"] for group in official_song_groups.values() for song in group
)

missing_official_songs_by_exact_title = official_song_titles - set(
    local_difficulties.keys()
)

# these are potential matches for missing official songs
local_matches = {}

# these are official songs which have no close matches locally
unmatched_official_songs = set()

for missing_official_title in missing_official_songs_by_exact_title:
    matches = difflib.get_close_matches(
        missing_official_title, local_difficulties.keys(), n=3, cutoff=0.6
    )

    if not matches:
        unmatched_official_songs.add(missing_official_title)
        continue

    def normalize_title(title: str) -> str:
        return (
            title.replace("！", "!")
            .replace("《", "<<")
            .replace("＜＜", "<<")
            .replace("》", ">>")
            .replace("＞＞", ">>")
            .replace("：", ":")
            .replace("’", "'")
            .replace("”", '"')
            .replace("''", '"')  # this one is dumb lol
            .replace("…", "...")
            .replace("｜｜", "||")
            .replace("＝", "=")
            .replace("～", "~")  # i'm upset that both of these are different
            .replace("〜", "~")
            # for PROVOES*PROPOSE <<êl fine>> - i'm no bothering with every accent lol
            .replace("ê", "e")
            .replace(" ", "")
            .lower()
        )

    # add the official titles of songs which match by some trivial criteria
    is_trivial_match = any(
        normalize_title(missing_official_title) == normalize_title(match)
        for match in matches
    )

    if is_trivial_match:
        local_difficulties[missing_official_title] = local_difficulties[matches[0]]
        continue

    # if it's not a trivial match, log it for manual review
    local_matches[missing_official_title] = matches[0]

print("local matches:", json.dumps(local_matches, ensure_ascii=False, indent=2))
print(
    "not found locally:",
    json.dumps(list(unmatched_official_songs), ensure_ascii=False, indent=2),
)

# { official_title: local_title }
manual_inclusions = {
    # i don't know what these *N things are, but we'll count them
    "月光乱舞*3": "月光乱舞",
    "ごりらがいるんだ*2": "ごりらがいるんだ",
    # i don't know about this one? close enough tbh
    "fancy cake!!": "fancy cake",
    # just moved the title credit into the artist field, lol
    "ARROW RAIN feat. ayame": "ARROW RAIN",
    "Alice Maestera feat. nomico": "Alice Maestera",
    # genuinely how do you fuck this up
    "プレインエイジア(MRM REMIX)": "プレインエイジア-MRM REMIX-",
    "POSSESSION(Gowrock Remix)": "POSSESSION -Gowrock Remix-",
    "トーホータノシ (feat. 抹)": "トーホータノシ feat. 抹",
    # haha ha unicode
    "Help me, ERINNNNNN!! #幻想郷ホロイズムver.": "Help me, ERINNNNNN!! #幻想郷ホロイズムver​.",
    "おにいちゃんグリッチホップ ～eternal love remix～": "おにいちゃんグリッチホップ 〜eternal love remix〜",
    # accidental hyphen?? in the official sources???
    "50th Memorial Songs -二人の時 ～under the cherry blossoms～-": "50th Memorial Songs -二人の時 ～under the cherry blossoms～",
    # what the fuck happened here??
    "劇場版ムーニャポヨポヨスッポコニャーゴ~侵略だいず帝国！ドラマティック宇宙大戦争~": "劇場版ムーニャポヨポヨスッポコニャーゴ‾侵略だいず帝国！ドラマティック宇宙大戦争‾",
    # ????????????????????
    "MΔX FLAVØR": "MΔX FLAV驩R",
}

for official_title, local_title in manual_inclusions.items():
    local_difficulties[official_title] = local_difficulties[local_title]


args.output_file.write_text(
    json.dumps(
        {
            title: list(difficulties)
            for title, difficulties in local_difficulties.items()
            if title in official_song_titles
        },
        ensure_ascii=False,
    ),
    encoding="utf-8",
    errors="ignore",
)
