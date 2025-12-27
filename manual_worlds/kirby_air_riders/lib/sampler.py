from dataclasses import dataclass, field
from typing import ClassVar, Iterable


class Sampler:
    @dataclass
    class Sample:
        item_names: set[str]
        location_names: set[str]

    _samplers_by_player: ClassVar[dict[int, "Sampler"]]

    @classmethod
    def pool_for(cls, player: int):
        return cls._samplers_by_player.setdefault(player, Sampler())

    def __init__(self) -> None:
        self.samples: list[Sampler.Sample] = []

    def add(self, samples: Iterable["Sampler.Sample"]):
        self.samples.extend(samples)

    @property
    def enabled_item_names(self):
        return {name for chart in self.samples for name in chart.item_names}

    @property
    def enabled_location_names(self):
        return {name for chart in self.samples for name in chart.location_names}
