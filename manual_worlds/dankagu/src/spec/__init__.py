from dataclasses import dataclass
from typing import NotRequired, TypedDict
from .songs import songs
from .world import WorldSpec
from .map import map_graph


def __define_world_spec():
    spec = WorldSpec()

    spec.define_location(
        "Restore Gensokyo",
        category="Victory",
        requires=f"|@Restoration:all|",
        victory=True,
    )

    spec.define_item(
        "Dream Drop",
        category="Dream Drops",
        progression=True,
        count=40,
    )

    for dlc_number in range(1, 12 + 1):
        (dlc_option, _) = spec.define_toggle_option(
            f"enable_dlc_{dlc_number}",
            display_name=f"Enable DLC {dlc_number}",
            description=f"Enables items and locations for DLC {dlc_number}",
            default=False,
            group="DLC",
        )
        spec.define_category(
            f"DLC {dlc_number}",
            yaml_option=[dlc_option],
            hidden=True,
        )

    (free_dlc_option, _) = spec.define_toggle_option(
        f"enable_free_dlc",
        display_name=f"Enable free DLC",
        description=f"Enables items and locations for free DLC",
        group="DLC",
        default=False,
    )
    spec.define_category(
        f"Free DLC",
        yaml_option=[free_dlc_option],
        hidden=True,
    )

    for area_number, spot_graph in map_graph.items():
        (area_restoration_category, _) = spec.define_category(
            f"Restoration (Area {area_number})",
            hidden=True,
        )

        (area_region_name, area_region) = spec.define_region(f"Area {area_number}")

        if area_number > 0:
            area_region["requires"] = f"|@Restoration (Area {area_number - 1}):all|"
            if area_number == 4:
                area_region["requires"] += " and |Dream Drop:80%|"

        if area_number < 4:
            area_region["connects_to"] = [f"Area {area_number + 1}"]

        for spot_name, spot_node in spot_graph.items():
            stage_graph = spot_node["stages"]
            spot_categories = [f"Area {area_number} - {spot_name}"]

            spot_progression = None

            # setting required_clears to 0 effectively means this spot is not required for restoration
            # useful for anything story-optional, like DLC or special achievement side quests
            if spot_node["required_clears"] > 0:
                spot_progression = spec.define_item(
                    f"{spot_name} Progression",
                    category=f"Spot Progression",
                    progression=True,
                    count=max(
                        spot_node["required_clears"],
                        *(stage.get("requires", 0) for stage in stage_graph.values()),
                    ),
                    early=area_number == 0,
                )["name"]

                spot_restoration = spec.define_item(
                    f"Restored {spot_name}",
                    category=["Restoration", area_restoration_category],
                    progression=True,
                )["name"]

                spot_restoration_location = spec.define_location(
                    f"Restore {spot_name}",
                    category=spot_categories,
                    region=area_region_name,
                    place_item=[spot_restoration],
                )

                spot_restoration_location["requires"] = (
                    f"|{spot_progression}:{spot_node["required_clears"]}|"
                )

            for stage_number, stage_data in stage_graph.items():
                stage_categories = spot_categories.copy()
                if "dlc" in stage_data:
                    stage_categories.append(f"DLC {stage_data['dlc']}")

                stage_location = spec.define_location(
                    f"Clear {spot_name} {stage_number}",
                    category=stage_categories,
                    region=area_region_name,
                )
                # spec.define_location(
                #     f"Clear {spot_name} {stage_number} Mission",
                #     category=stage_categories,
                #     region=area_region_name,
                # )

                if "requires" in stage_data and spot_progression:
                    stage_location["requires"] = (
                        f"|{spot_progression}:{stage_data['requires']}|"
                    )

    @dataclass
    class CharacterData(TypedDict):
        name: str
        spot: str
        stage: int
        dlc: NotRequired[int]

    characters: list[CharacterData] = [
        # {"name": "Reimu Hakurei" },
        {"name": "Marisa Kirisame", "spot": "Hakurei Shrine", "stage": 3},
        {"name": "Cirno", "spot": "Misty Lake", "stage": 4},
        {"name": "Sakuya Izayoi", "spot": "Scarlet Devil Mansion", "stage": 7},
        {"name": "Remilia Scarlet", "spot": "Scarlet Devil Mansion", "stage": 11},
        {"name": "Flandre Scarlet", "spot": "Scarlet Devil Mansion", "stage": 13},
        {"name": "Alice Margatroid", "spot": "Forest of Magic", "stage": 4},
        {"name": "Youmu Konpaku", "spot": "Hades", "stage": 4},
        {"name": "Yuyuko Saigyouji", "spot": "Hades", "stage": 12},
        {"name": "Yukari Yakumo", "spot": "Hakurei Shrine", "stage": 3},
        {
            "name": "Reisen Udongein Inaba",
            "spot": "Bamboo Forest of the Lost",
            "stage": 3,
        },
        {"name": "Kaguya Houraisan", "spot": "Eientei", "stage": 4},
        {"name": "Fujiwara no Mokou", "spot": "Human Village", "stage": 4},
        {"name": "Aya Shameimaru", "spot": "Youkai Mountain", "stage": 7},
        {"name": "Sanae Kochiya", "spot": "Moriya Shrine", "stage": 4},
        {"name": "Tenshi Hinanawi", "spot": "Heaven", "stage": 6},
        {"name": "Satori Komeiji", "spot": "Underworld", "stage": 6},
        {"name": "Utsuho Reiuji", "spot": "Underworld", "stage": 11},
        {"name": "Koishi Komeiji", "spot": "Underworld", "stage": 10},
        {"name": "Byakuren Hijiri", "spot": "Myouren Temple", "stage": 5},
        # {"name": "Toyosatomimi no Miko", "spot": "Senkai", "stage": 7, "dlc": 2},
    ]

    # for character in characters:
    #     spec.define_location(
    #         f"Unlock {character['name']}",
    #         category=["Characters"]
    #         + ("dlc" in character and [f"DLC {character['dlc']}"] or []),
    #         requires=f"|{character['spot']} Progression:{character['stage']}|",
    #     )

    songs_category = "Free Play"
    (base_songs_category, _) = spec.define_category("Base Songs", hidden=True)

    groups_by_song: dict[str, list[str]] = {}
    for song_data in songs:
        song_title = song_data["title"]
        if song_title not in groups_by_song:
            groups_by_song[song_title] = []

        song_dlc = song_data.get("dlc", None)

        groups_by_song[song_title].append(
            song_dlc == "free"
            and "Free DLC"
            or song_dlc != None
            and f"DLC {song_dlc}"
            or base_songs_category
        )

    for song_index, (song_name, group_names) in enumerate(groups_by_song.items()):
        (song_category, _) = spec.define_category(f"Song {song_index}", hidden=True)

        for song_group_name in group_names:
            item_name = song_name
            if item_name in spec.items:
                item_name += " (Free Play)"

            spec.define_item(
                item_name,
                category=[songs_category, song_group_name, song_category],
                progression=True,
            )

            song_requires = f"|{item_name}|"
            if any(char in item_name for char in ":|"):
                song_requires = f"|@{song_category}|"

            spec.define_location(
                item_name,
                category=[songs_category, song_group_name, song_category],
                requires=song_requires,
            )

    spec.game["starting_items"] = [
        {"item_categories": [songs_category], "random": 5},
    ]

    return spec


spec = __define_world_spec()
