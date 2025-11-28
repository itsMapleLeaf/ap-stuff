from tracemalloc import start
from ..lib.world import WorldSpec
from ..lib.requires import Requires


class VisualNovelsWorldSpec(WorldSpec):
    def __init__(self):
        super().__init__(
            game="VisualNovelsGardync6",
            creator="MapleLeaf",
            filler_item_name="Useless Filler Item",
        )

        self.progessive_arc_category = self.define_category(
            "Progressive Arc", starting_count=1
        )[0]

        self.define_visual_novel("The Way We All Go")
        self.define_visual_novel("Her Love, Like Poison")
        self.define_visual_novel("How to Melt a Maiden's Heart")
        self.define_visual_novel("Rain and the Wolf")

        self.define_location(
            "Finish",
            category="Victory",
            victory=True,
        )

    def define_visual_novel(self, name: str):
        # since I haven't actually played these, this is just a total guess
        # if the game has fewer arcs, higher arcs are free
        # if the game has more arcs, the rest of the game is unlocked by the last arc location
        arc_count = 5

        arc_item = self.define_item(
            f"{name} - Progressive Arc",
            category=self.progessive_arc_category,
            progression=True,
            count=arc_count,
        )

        for arc_number in range(1, arc_count + 1):
            self.define_location(
                f"{name} - Finish Arc {arc_number}",
                category=f"Visual Novels - {name}",
                requires=Requires.item(arc_item, arc_number),
            )


world_spec = VisualNovelsWorldSpec()
