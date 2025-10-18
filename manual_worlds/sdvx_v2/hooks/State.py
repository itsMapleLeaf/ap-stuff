from dataclasses import dataclass
from typing import ClassVar, Iterable
from ..spec import SongSpec


class ChartPool:
    _pools_by_player: ClassVar[dict[int, "ChartPool"]] = {}

    @classmethod
    def for_player(cls, player: int):
        return cls._pools_by_player.setdefault(player, ChartPool())

    def __init__(self) -> None:
        self.charts: list[SongSpec.Chart] = []

    def add_charts(self, charts: Iterable[SongSpec.Chart]):
        self.charts.extend(charts)

    @property
    def enabled_item_names(self):
        return {chart.item_name for chart in self.charts}

    @property
    def enabled_location_names(self):
        return {name for chart in self.charts for name in chart.location_names}
