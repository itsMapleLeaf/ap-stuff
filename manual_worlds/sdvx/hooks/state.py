from dataclasses import dataclass
from random import Random
from typing import ClassVar, Iterable
from ..spec import SongSpec


class ChartPool:
    _pools_by_player: ClassVar[dict[int, "ChartPool"]] = {}

    @classmethod
    def for_player(cls, player: int):
        return cls._pools_by_player.setdefault(player, ChartPool())

    def __init__(self) -> None:
        self.charts: list[SongSpec.Chart] = []
        self.goal_chart: SongSpec.Chart

    def add_charts(self, charts: Iterable[SongSpec.Chart]):
        self.charts.extend(charts)

    def choose_goal_chart(
        self, random: Random, goal_level: int
    ):
        self.goal_chart = random.choice(
            [
                chart
                for chart in self.charts
                if  chart.level == goal_level
            ]
        )

    @property
    def goal_song_location_names(self):
        return self.goal_chart.location_names

    @property
    def enabled_item_names(self):
        return {chart.song.item_name for chart in self.charts}

    @property
    def enabled_location_names(self):
        return {name for chart in self.charts for name in chart.location_names}
