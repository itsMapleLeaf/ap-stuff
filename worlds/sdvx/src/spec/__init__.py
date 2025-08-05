import json
from pathlib import Path
from .world import WorldSpec
from .songs import Song
from .config import song_goals, song_brackets


def __load_songs() -> list[Song]:
    from ..Helpers import load_data_file

    data: object = load_data_file("songs.json")

    if not isinstance(data, list):
        raise Exception("song data must be a list")

    return [Song(**item) for item in data]


def __define_world_spec(songs: list[Song]) -> WorldSpec:
    song_titles = set[str]()
    duplicate_song_titles = set[str]()

    for song in songs:
        if not song.title in song_titles:
            song_titles.add(song.title)
        else:
            duplicate_song_titles.add(song.title)

    songs_item_category = "Songs"

    world_spec = WorldSpec(
        starting_items=[
            {"item_categories": [songs_item_category], "random": 5},
        ]
    )

    for song in songs:
        world_spec.define_category(
            song.id_category_name,
            hidden=True,
        )

        song_item_name = (
            song.title
            if not song.title in duplicate_song_titles
            else f"{song.title} (by {song.artist})"
        )

        song_location_category_name = f"Songs - {song_item_name}"

        world_spec.define_item(
            song_item_name,
            category=[song.id_category_name, songs_item_category],
            progression=True,
        )

        world_spec.define_location(
            f"{song_item_name} - Track Clear",
            category=[song_location_category_name, song.id_category_name],
            requires=f"|@{song.id_category_name}|",
        )

        for song_goal in song_goals:
            song_volforce_item_name = world_spec.define_item(
                f"{song_item_name} - {song_goal.name}",
                category=["Song Completion", song.id_category_name],
                progression=True,
                value={"volforce": song_goal.volforce},
            )["name"]

            world_spec.define_location(
                f"{song_item_name} - {song_goal.name}",
                category=[song_location_category_name, song.id_category_name],
                requires=f"|@{song.id_category_name}|",
                place_item=[song_volforce_item_name],
            )

    world_spec.define_location(
        "MAX VOLFORCE",
        category="Victory",
        requires="{ItemValue(volforce:700)}",
        victory=True,
    )

    return world_spec


songs = __load_songs()
spec = __define_world_spec(songs)
