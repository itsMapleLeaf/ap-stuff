from dataclasses import InitVar, dataclass, field
from functools import reduce
import re
from typing import Iterable, NotRequired, Optional, TypedDict
from .songs import song_groups_to_songs
from .world import WorldSpec
from .map import map_graph


def __define_world_spec():
    areas: list["Area"] = []

    @dataclass
    class Area:
        id: int | str
        starting: bool = False
        required_clears: list[tuple["Spot", int]] | None = None
        connections: list["Area"] = field(init=False, default_factory=list)
        spots: list["Spot"] = field(init=False, default_factory=list)

        def __post_init__(self):
            areas.append(self)

        @property
        def name(self) -> str:
            return f"Area {self.id}" if isinstance(self.id, int) else self.id

        def connection(
            self, id: int | str, required_clears: list[tuple["Spot", int]] | None = None
        ):
            area = Area(
                id,
                required_clears=required_clears,
            )
            self.connections.append(area)
            return area

        def spot(self, name: str):
            spot = Spot(self, name)
            self.spots.append(spot)
            return spot

    @dataclass
    class Spot:
        area: Area
        name: str
        stages: list["Stage"] = field(init=False, default_factory=list)

        @property
        def category(self) -> str:
            return f"{self.area.name} - {self.name}"

        def stage(self, id: str | int, requires: Optional["Stage"] = None):
            stage = Stage(self, id, requires)
            self.stages.append(stage)
            return stage

    @dataclass
    class Stage:
        spot: Spot
        id: str | int
        requires: Optional["Stage"]

        @property
        def name(self) -> str:
            return (
                f"{self.spot.name} - Stage {self.id:02d}"
                if isinstance(self.id, int)
                else self.id
            )

        @property
        def unlocks_region_name(self) -> str:
            return f"{self.name} Unlocks"

    area_0 = Area(0, starting=True)

    hakurei_shrine = area_0.spot("Hakurei Shrine")

    hakurei_shrine_1 = hakurei_shrine.stage(1)
    hakurei_shrine_2 = hakurei_shrine.stage(2)
    hakurei_shrine_3 = hakurei_shrine.stage(3)
    hakurei_shrine_4 = hakurei_shrine.stage(4, requires=hakurei_shrine_2)
    hakurei_shrine_5 = hakurei_shrine.stage(5, requires=hakurei_shrine_2)
    hakurei_shrine_6 = hakurei_shrine.stage(6, requires=hakurei_shrine_5)
    hakurei_shrine_7 = hakurei_shrine.stage(7, requires=hakurei_shrine_5)

    area_1 = area_0.connection(1, required_clears=[(hakurei_shrine, 3)])

    # TODO

    area_2 = area_1.connection(2)

    # TODO

    area_3 = area_2.connection(3)

    # TODO

    area_4 = area_3.connection(4)

    hakurei_shrine_reconstruction = area_4.spot("Hakurei Shrine - Reconstruction")

    white_world = hakurei_shrine_reconstruction.stage(1)

    hakurei_shrine_8 = hakurei_shrine_reconstruction.stage(8, requires=white_world)
    hakurei_shrine_9 = hakurei_shrine_reconstruction.stage(9, requires=white_world)
    hakurei_shrine_10 = hakurei_shrine_reconstruction.stage(10, requires=white_world)
    hakurei_shrine_11 = hakurei_shrine_reconstruction.stage(11, requires=white_world)

    spec = WorldSpec()

    for area in areas:
        (_, region) = spec.define_region(
            area.name,
            starting=area.starting,
            connects_to=[connection.name for connection in area.connections],
        )

        if area.required_clears:
            region["requires"] = " and ".join(
                f"|@{spot.category}:{count}|" for spot, count in area.required_clears
            )

        for spot in area.spots:
            for stage in spot.stages:
                spec.define_item(
                    stage.name,
                    category=[
                        stage.spot.area.name,
                        f"{stage.spot.area.name} - {stage.spot.name}",
                    ],
                    progression=True,
                )

                spec.define_location(
                    stage.name,
                    category=f"{stage.spot.area.name} - {stage.spot.name}",
                    requires=f"|{stage.name}|",
                    region=(
                        stage.requires.unlocks_region_name
                        if stage.requires
                        else stage.spot.area.name
                    ),
                )

    # spec.define_item(
    #     "Hakurei Shrine - Stage 02",
    #     category="Area 0",
    #     progression=True,
    # )
    # spec.define_location(
    #     "Hakurei Shrine - Stage 02",
    #     category="Area 0 - Hakurei Shrine",
    #     requires="|Hakurei Shrine - Stage 02|",
    #     region="Area 0",
    # )

    # spec.define_item(
    #     "Hakurei Shrine - Stage 03",
    #     category="Area 0",
    #     progression=True,
    # )
    # spec.define_location(
    #     "Hakurei Shrine - Stage 03",
    #     category="Area 0 - Hakurei Shrine",
    #     requires="|Hakurei Shrine - Stage 03|",
    #     region="Area 0",
    # )

    # spec.define_item(
    #     "Hakurei Shrine - Stage 04",
    #     category="Area 0",
    #     progression=True,
    # )
    # spec.define_location(
    #     "Hakurei Shrine - Stage 04",
    #     category="Area 0 - Hakurei Shrine",
    #     requires="|Hakurei Shrine - Stage 04|",
    #     region="Hakurei Shrine - Stage 02 Unlocks",
    # )

    # spec.define_item(
    #     "Hakurei Shrine - Stage 05",
    #     category="Area 0",
    #     progression=True,
    # )
    # spec.define_location(
    #     "Hakurei Shrine - Stage 05",
    #     category="Area 0 - Hakurei Shrine",
    #     requires="|Hakurei Shrine - Stage 05|",
    #     region="Hakurei Shrine - Stage 02 Unlocks",
    # )

    # spec.define_region(
    #     "Area 0 - Hakurei Shrine - Stage 02",
    #     requires=f"|Hakurei Shrine - Stage 02|",
    # )

    # spec.define_region(
    #     "Area 0 - Hakurei Shrine - Stage 05",
    #     requires=f"|Hakurei Shrine - Stage 05|",
    # )

    # spec.define_region(
    #     "Area 1",
    #     connects_to=[
    #         "Area 1 - Scarlet Devil Mansion - Stage 01",
    #         "Area 1 - Scarlet Devil Mansion - Stage 02",
    #         "Area 1 - Scarlet Devil Mansion - Stage 06",
    #         "Area 1 - Scarlet Devil Mansion - Stage 14",
    #         "Area 2",
    #     ],
    #     requires=f"|@Area 0 Clear|",
    # )
    # spec.define_region(
    #     "Area 1 - Scarlet Devil Mansion - Stage 01",
    #     requires=f"|Scarlet Devil Mansion - Stage 01|",
    # )
    # spec.define_region(
    #     "Area 1 - Scarlet Devil Mansion - Stage 02",
    #     requires=f"|Scarlet Devil Mansion - Stage 02|",
    # )
    # spec.define_region(
    #     "Area 1 - Scarlet Devil Mansion - Stage 06",
    #     requires=f"|Scarlet Devil Mansion - Stage 06|",
    # )
    # spec.define_region(
    #     "Area 1 - Scarlet Devil Mansion - Stage 14",
    #     requires=f"|Scarlet Devil Mansion - Stage 14|",
    # )

    # spec.define_item(
    #     "Hakurei Shrine - Stage 01",
    #     category="Area 0 - Hakurei Shrine",
    #     progression=True,
    # )

    # spec.define_location(
    #     "Hakurei Shrine - Stage 01",
    #     category="Area 0 - Hakurei Shrine",
    # )

    # spec.define_location(
    #     "Hakurei Shrine - Stage 02",
    #     category="Area 0 - Hakurei Shrine",
    # )

    # spec.define_location(
    #     "Hakurei Shrine - Stage 03",
    #     category="Area 0 - Hakurei Shrine",
    # )

    # spec.define_location(
    #     "Hakurei Shrine - Stage 04",
    #     category="Area 0 - Hakurei Shrine",
    #     requires=f"|Hakurei Shrine - Stage 02|",
    # )

    free_play_category = "Free Play"

    spec.game.setdefault("starting_items", []).append(
        {"item_categories": [free_play_category], "random": 5},
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
