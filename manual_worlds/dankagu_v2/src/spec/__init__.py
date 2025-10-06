from dataclasses import dataclass
from functools import reduce
import re
from typing import Iterable, NotRequired, TypedDict
from .songs import song_groups_to_songs
from .world import WorldSpec
from .map import map_graph


def __define_world_spec():
    free_play_category = "Free Play"

    spec = WorldSpec(
        starting_items=[
            {"item_categories": [free_play_category], "random": 5},
        ]
    )

    group_categories: dict[str, str] = {}

    for group_name, song_names in song_groups_to_songs.items():
        (group_option, _) = spec.define_toggle_option(
            __song_group_option_name(group_name),
            display_name=f"{group_name} Free Play",
            description=f"Enables items and locations for Free Play with songs from {group_name}.",
            default=False,
        )

        (group_categories[group_name], _) = spec.define_category(
            f"Free Play - {group_name}",
            hidden=True,
            yaml_option=[group_option],
        )

    songs_to_groups: dict[str, set[str]] = {}
    for group_name, song_names in song_groups_to_songs.items():
        for song_name in song_names:
            songs_to_groups.setdefault(song_name, set()).add(group_name)

    for song_name, song_groups in songs_to_groups.items():
        song_categories: list[str] = [
            free_play_category,
            *(group_categories[group] for group in song_groups),
        ]

        song_item = spec.define_item(
            re.sub(r"[:|]", " ", song_name),
            category=song_categories,
            progression=True,
        )["name"]

        spec.define_location(
            song_name,
            category=song_categories,
            requires=f"|{song_item}|",
        )

    spec.define_location(
        "Restore Gensokyo",
        category="Victory",
        victory=True,
    )

    return spec


def __song_group_option_name(group_name: str):
    return f"{__snake_case(group_name)}_free_play"


def __snake_case(text: str) -> str:
    return "_".join(
        part.group(0).lower() for part in re.finditer(r"[A-Z]*[a-z0-9]+", text)
    )


def __counts[T](values: Iterable[T]) -> dict[T, int]:
    counts: dict[T, int] = {}
    for value in values:
        counts[value] = counts.setdefault(value, 0) + 1
    return counts


def __duplicates[T](values: Iterable[T]) -> set[T]:
    return {value for value, count in __counts(values).items() if count >= 2}


spec = __define_world_spec()
