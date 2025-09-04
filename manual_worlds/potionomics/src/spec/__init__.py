from dataclasses import dataclass
from typing import ClassVar, cast

from .world import WorldSpec
from ..Helpers import load_data_file


class PotionomicsWorldSpec(WorldSpec):
    @dataclass
    class IngredientSpec:
        name: str
        a: int
        b: int
        c: int
        d: int
        e: int
        total_magimin: int
        price_quinn: str
        value: float
        taste: str | None
        touch: str | None
        smell: str | None
        sight: str | None
        sound: str | None
        price_mod: str
        type: str
        rarity: str
        location: str

    ingredients = {}
    for ingredient_data in cast(
        list[dict], load_data_file("potionomics_ingredients.json")
    ):
        ingredients[str(ingredient_data["name"])] = IngredientSpec(**ingredient_data)

    potions: ClassVar = {
        "Health Potion",
        "Mana Potion",
        "Stamina Potion",
        "Speed Potion",
        "Tolerance Potion",
        "Fire Tonic",
        "Ice Tonic",
        "Thunder Tonic",
        "Shadow Tonic",
        "Radiation Tonic",
        "Sight Enhancer",
        "Alertness Enhancer",
        "Insight Enhancer",
        "Dowsing Enhancer",
        "Seeking Enhancer",
        "Poison Cure",
        "Drowsiness Cure",
        "Petrification Cure",
        "Silence Cure",
        "Curse Cure",
    }

    @dataclass
    class PotionTierSpec:
        magimins: tuple[int, int, int, int, int, int]
        """The amount of magimins required for each star rating in this tier, from 0 to 5"""

    potion_tiers: ClassVar = {
        "Minor": PotionTierSpec((0, 10, 20, 30, 40, 50)),
        "Common": PotionTierSpec((60, 75, 90, 105, 115, 130)),
        "Greater": PotionTierSpec((150, 170, 195, 215, 235, 260)),
        "Grand": PotionTierSpec((290, 315, 345, 370, 400, 430)),
        "Superior": PotionTierSpec((470, 505, 545, 580, 620, 660)),
        "Masterwork": PotionTierSpec((720, 800, 875, 960, 1040, 1121)),
    }

    @dataclass
    class CardSpec:
        rank: int

    @dataclass
    class CharacterSpec:
        name: str
        chapter: int
        cards: dict[str, "PotionomicsWorldSpec.CardSpec"]

        @property
        def item_name(self) -> str:
            return f"{self.name} (Progressive Character)"

    starting_relationship_rank = 2
    max_relationship_rank = 10

    characters: ClassVar = {
        character.name: character
        for character in [
            CharacterSpec(
                "Quinn",
                chapter=1,
                cards={
                    "Hustle": CardSpec(rank=1),
                    "Take It or Leave It": CardSpec(rank=2),
                    "Shock Factor": CardSpec(rank=3),
                    "Plant the Seed": CardSpec(rank=4),
                    "Press the Attack": CardSpec(rank=5),
                    "Pressure": CardSpec(rank=6),
                    "Fuel the Fire": CardSpec(rank=7),
                    "Compound Interest": CardSpec(rank=8),
                },
            ),
            CharacterSpec(
                "Mint",
                chapter=1,
                cards={
                    "Sympathy": CardSpec(rank=1),
                    "Keep Your Guard Up": CardSpec(rank=2),
                    "Muscle Memory": CardSpec(rank=3),
                    "Blitz": CardSpec(rank=5),
                    "Eye on the Prize": CardSpec(rank=6),
                    "Fortitude": CardSpec(rank=7),
                    "Unfazed": CardSpec(rank=9),
                    "Keep It Simple": CardSpec(rank=1),
                },
            ),
            CharacterSpec(
                "Baptiste",
                chapter=1,
                cards={
                    "Captivate": CardSpec(rank=1),
                    "Build Rapport": CardSpec(rank=2),
                    "Subvert": CardSpec(rank=3),
                    "Compromise": CardSpec(rank=5),
                    "Common Ground": CardSpec(rank=6),
                    "Strategic Withdrawal": CardSpec(rank=7),
                    "Emotional Intelligence": CardSpec(rank=9),
                    "Silver Tongue": CardSpec(rank=10),
                },
            ),
            CharacterSpec(
                "Muktuk",
                chapter=1,
                cards={
                    "Pump Up": CardSpec(rank=1),
                    "Enthusiasm": CardSpec(rank=2),
                    "Craftsmanship": CardSpec(rank=3),
                    "Reinforce": CardSpec(rank=4),
                    "Bravado": CardSpec(rank=5),
                    "Zeal": CardSpec(rank=7),
                    "Artistry": CardSpec(rank=9),
                    "Conviction": CardSpec(rank=10),
                },
            ),
            CharacterSpec(
                "Saffron",
                chapter=1,
                cards={
                    "Meditate": CardSpec(rank=1),
                    "Guided Thought": CardSpec(rank=2),
                    "Casual Conversation": CardSpec(rank=3),
                    "Deep Connection": CardSpec(rank=5),
                    "Mindfulness": CardSpec(rank=6),
                    "Regulated Breathing": CardSpec(rank=7),
                    "Serenity of the Mind": CardSpec(rank=9),
                    "Tranquility": CardSpec(rank=10),
                },
            ),
            CharacterSpec(
                "Roxanne",
                chapter=2,
                cards={
                    "Sleight of Hand": CardSpec(rank=1),
                    "Flattery": CardSpec(rank=2),
                    "Disarm": CardSpec(rank=3),
                    "Pander": CardSpec(rank=5),
                    "Emotional Mindfield": CardSpec(rank=6),
                    "Chapstick": CardSpec(rank=7),
                    "Magnetism": CardSpec(rank=9),
                    "Mass Misdirection": CardSpec(rank=10),
                },
            ),
            CharacterSpec(
                "Xidriel",
                chapter=2,
                cards={
                    "Jingle": CardSpec(rank=1),
                    "Opening Act": CardSpec(rank=2),
                    "Chorus": CardSpec(rank=3),
                    "Improv": CardSpec(rank=5),
                    "Rhythm": CardSpec(rank=6),
                    "Throat Spray": CardSpec(rank=7),
                    "Catchy Tune": CardSpec(rank=9),
                    "Encore": CardSpec(rank=10),
                },
            ),
            CharacterSpec(
                "Salt & Pepper",
                chapter=2,
                cards={
                    "Strike or Strike Later": CardSpec(rank=1),
                    "Good Cop, Bad Cop": CardSpec(rank=2),
                    "Salt or Pepper": CardSpec(rank=3),
                    "Avast Ye!": CardSpec(rank=5),
                    "Give No Quarter": CardSpec(rank=6),
                    "Batten Down the Hatches": CardSpec(rank=7),
                    "Mental Purrrley": CardSpec(rank=9),
                    "Carpe Diem": CardSpec(rank=10),
                },
            ),
            CharacterSpec(
                "Corsac",
                chapter=3,
                cards={
                    "Ferocity of the Squirrel": CardSpec(rank=1),
                    "Adapt": CardSpec(rank=2),
                    "Be Prepared": CardSpec(rank=3),
                    "Happy Place": CardSpec(rank=5),
                    "Serenity of the Mollus": CardSpec(rank=6),
                    "Pivot": CardSpec(rank=7),
                    "Mind of the Slime": CardSpec(rank=9),
                    "Lessons from Nature": CardSpec(rank=10),
                },
            ),
            CharacterSpec(
                "Luna",
                chapter=3,
                cards={
                    "Elevator Pitch": CardSpec(rank=1),
                    "Lean into It": CardSpec(rank=2),
                    "Wing It": CardSpec(rank=3),
                    "Rehearsed Line": CardSpec(rank=5),
                    "Caffeine Rush": CardSpec(rank=6),
                    "Dig Deep": CardSpec(rank=7),
                    "Subliminal Suggestion": CardSpec(rank=9),
                    "Final Push": CardSpec(rank=10),
                },
            ),
        ]
    }

    banned_cards = {
        "Regulated Breathing",
        "Serenity of the Mind",
        "Chorus",
        # "Rattle 'Em Off",
    }
    for character in characters.values():
        for banned_card_name in banned_cards:
            if banned_card_name in character.cards:
                character.cards.pop(banned_card_name)

    @dataclass
    class AdventureLocationSpec:
        chapter: int

    adventure_locations: ClassVar = {
        "Enchanted Forest": AdventureLocationSpec(chapter=1),
        "Bone Wastes": AdventureLocationSpec(chapter=1),
        "Mushroom Mire": AdventureLocationSpec(chapter=1),
        "Shadow Steppe": AdventureLocationSpec(chapter=2),
        "Ocean Coasts": AdventureLocationSpec(chapter=2),
        "Storm Plains": AdventureLocationSpec(chapter=2),
        "Sulfuric Falls": AdventureLocationSpec(chapter=3),
        "Crystalline Forest": AdventureLocationSpec(chapter=3),
        "Ice Craggs": AdventureLocationSpec(chapter=3),
        "Dragon Oasis": AdventureLocationSpec(chapter=4),
        "Crater": AdventureLocationSpec(chapter=4),
        "Arctic": AdventureLocationSpec(chapter=4),
        "Magical Wasteland": AdventureLocationSpec(chapter=5),
    }

    @dataclass
    class CauldronSpec:
        chapter: int

        @property
        def required_progressive_item_count(self) -> int:
            return (self.chapter - 1) * 3

    cauldrons: ClassVar[dict[str, CauldronSpec]] = {
        "Mudpack Cauldron": CauldronSpec(chapter=1),
        "Glass Cauldron": CauldronSpec(chapter=1),
        "Storm Cauldron": CauldronSpec(chapter=1),
        "Ocean Cauldron": CauldronSpec(chapter=2),
        "Shadow Cauldron": CauldronSpec(chapter=2),
        "Crystal Cauldron": CauldronSpec(chapter=2),
        "Steel Cauldron": CauldronSpec(chapter=3),
        "Celestial Cauldron": CauldronSpec(chapter=3),
        "Arctic Cauldron": CauldronSpec(chapter=3),
        "Crater Cauldron": CauldronSpec(chapter=4),
        "Dragon Cauldron": CauldronSpec(chapter=4),
        "Magical Wasteland Cauldron": CauldronSpec(chapter=5),
    }

    @dataclass
    class ShelfSpec:
        chapter: int

    shelves: ClassVar = {
        "Mushroom Mire Shelf": ShelfSpec(chapter=1),
        "Bone Wastes Shelf": ShelfSpec(chapter=1),
        "Storm Plains Shelf": ShelfSpec(chapter=1),
        "Ocean Coasts Shelf": ShelfSpec(chapter=2),
        "Shadow Steppe Shelf": ShelfSpec(chapter=2),
        "Sulfuric Falls Shelf": ShelfSpec(chapter=2),
        "Crystalline Forest Shelf": ShelfSpec(chapter=3),
        "Ice Craggs Shelf": ShelfSpec(chapter=3),
        "Crater Shelf": ShelfSpec(chapter=3),
        "Dragon Oasis Shelf": ShelfSpec(chapter=4),
        "Arctic Shelf": ShelfSpec(chapter=4),
        "Magical Wasteland Shelf": ShelfSpec(chapter=5),
    }

    @dataclass
    class ShopUpgradeSpec:
        upgrade_count: int = 0

    shop_upgrades: ClassVar = {
        "Shop Front": ShopUpgradeSpec(upgrade_count=3),
        "Brewing Area": ShopUpgradeSpec(upgrade_count=3),
        "Basement": ShopUpgradeSpec(upgrade_count=3),
    }

    showcases: ClassVar = {
        "Mushroom Mire Showcase",
        "Bone Wastes Showcase",
        "Storm Plains Showcase",
        "Ocean Coasts Showcase",
        "Shadow Steppe Showcase",
        "Sulfuric Falls Showcase",
        "Crystalline Forest Showcase",
        "Ice Craggs Showcase",
        "Crater Showcase",
        "Dragon Oasis Showcase",
        "Arctic Showcase",
        "Magical Wasteland Showcase",
    }

    barrels: ClassVar = {
        "Mushroom Barrel",
        "Cactus Barrel",
        "Thunder Log Barrel",
        "Coral Barrel",
        "Cocoon Barrel",
        "Vines Barrel",
        "Prismatic Timber Barrel",
        "Frost Kindling Barrel",
        "Poly Log Barrel",
        "Scaly Wood Barrel",
        "Yeti Pelt Barrel",
        "Empyrean Bud Barrel",
    }

    fuels: ClassVar = {
        "Hay",
        "Oak Wood",
        "Mushroom",
        "Cactus",
        "Thunder Log",
        "Coral",
        "Cocoon",
        "Vine",
        "Prismatic Timber",
        "Frost Kindling",
        "Poly Log",
        "Scaly Wood",
        "Yeti Pelt",
        "Empyrean Bud",
    }

    def __init__(self):
        progressive_items_category = "Progression"
        progressive_characters_category = "Characters"

        super().__init__(
            starting_items=[
                # you need mint to get the necessary ingredients to progress early game
                {"items": [self.characters["Mint"].item_name], "random": 1},
                # some other random jumpstart progression
                {"item_categories": [progressive_items_category], "random": 3},
                {"item_categories": [progressive_characters_category], "random": 3},
            ]
        )

        contest_count = 5

        contest_reward_item_name = self.define_item(
            "Contest Reward",
            category="Contest Rewards",
            progression=True,
            count=contest_count,
        )["name"]

        self.define_location(
            "Save the Shop",
            category="Victory!",
            requires=f"|{contest_reward_item_name}:all|",
            victory=True,
        )

        for contest_index in range(contest_count):
            self.define_location(
                f"Win Contest {contest_index + 1}",
                category="Contests",
                requires=f"|{contest_reward_item_name}:{contest_index}|",
                place_item=[contest_reward_item_name],
            )

        for potion in self.potions:
            potion_type = potion.split(" ")[-1]

            self.define_location(
                f"Brew {potion}",
                category=f"Brewing - {potion_type}s",
            )

            # for potion_tier in self.potion_tiers:
            #     self.define_location(
            #         f"Brew {potion_tier} {potion} or higher",
            #         category=f"Potions - {potion}",
            #     )

        for character_spec in self.characters.values():
            self.define_item(
                character_spec.item_name,
                category=[progressive_characters_category],
                progression=True,
                count=10,
            )

            self.define_location(
                f"{character_spec.name} - Reach Rank 7",
                category=f"Characters - {character_spec.name}",
                requires=f"|{character_spec.item_name}:1| and |{contest_reward_item_name}:{character_spec.chapter - 1}|",
            )

            self.define_location(
                f"{character_spec.name} - Reach Rank 10",
                category=f"Characters - {character_spec.name}",
                requires=f"|{character_spec.item_name}:1| and |{contest_reward_item_name}:{character_spec.chapter - 1}|",
            )

            # for relationship_rank in range(
            #     self.starting_relationship_rank, self.max_relationship_rank
            # ):
            #     self.define_location(
            #         f"{character_name} - Reach Rank {relationship_rank}",
            #         category=f"Characters - {character_name}",
            #         requires=f"|{progressive_characters_item_name}:{character_index + 1}|",
            #     )

        progressive_adventure_locations_item_name = self.define_item(
            "Progressive Adventure Locations",
            category=progressive_items_category,
            count=max(
                location.chapter for location in self.adventure_locations.values()
            ),
            progression=True,
        )["name"]

        for (
            adventure_location_name,
            adventure_location,
        ) in self.adventure_locations.items():
            adventurer_character_requirement = " or ".join(
                f"|{self.characters[name].item_name}|"
                for name in ["Mint", "Xidriel", "Corsac"]
            )

            self.define_location(
                f"Adventure in {adventure_location_name}",
                category=f"Adventure - Chapter {adventure_location.chapter}",
                requires=(
                    " and ".join(
                        [
                            f"({adventurer_character_requirement})",
                            f"|{progressive_adventure_locations_item_name}:{adventure_location.chapter}|",
                            f"|{contest_reward_item_name}:{adventure_location.chapter - 1}|",
                        ]
                    )
                ),
            )

        progressive_cauldron_item_name = self.define_item(
            "Progressive Cauldrons",
            category=progressive_items_category,
            progression=True,
            count=len(self.cauldrons),
        )["name"]

        for cauldron_name, cauldron_spec in self.cauldrons.items():
            for cauldron_upgrade_index in range(3):
                self.define_location(
                    f"Buy {cauldron_name}{"+" * cauldron_upgrade_index}",
                    category=[f"Cauldrons - Chapter {cauldron_spec.chapter}"],
                    requires=(
                        " and ".join(
                            [
                                f"|{self.characters['Muktuk'].item_name}|",
                                f"|{progressive_cauldron_item_name}:{cauldron_spec.required_progressive_item_count}|",
                                f"|{contest_reward_item_name}:{cauldron_spec.chapter - 1}|",
                            ]
                        )
                    ),
                )

        for shelf_name, shelf_spec in self.shelves.items():
            for shelf_upgrade_index in range(3):
                self.define_location(
                    f"Buy {shelf_name}{"+" * shelf_upgrade_index}",
                    category=f"Shelves - {shelf_name}",
                    requires=" and ".join(
                        [
                            f"|{self.characters['Muktuk'].item_name}|",
                            f"|{contest_reward_item_name}:{shelf_spec.chapter - 1}|",
                        ]
                    ),
                )

        for shop_upgrade_name, shop_upgrade_spec in self.shop_upgrades.items():
            # progressive_shop_upgrade_item_name = self.define_item(
            #     f"Progressive {shop_upgrade_name}",
            #     category=progressive_items_category,
            #     progression=True,
            #     count=shop_upgrade_spec.upgrade_count,
            # )["name"]

            for shop_upgrade_index in range(shop_upgrade_spec.upgrade_count):
                self.define_location(
                    f"Buy {shop_upgrade_name} Level {shop_upgrade_index + 2}",
                    category=f"Shop Upgrades - {shop_upgrade_name}",
                    requires=" and ".join(
                        [
                            f"|{self.characters['Saffron'].item_name}|",
                            # f"|{progressive_shop_upgrade_item_name}:{shop_upgrade_index + 1}|",
                        ]
                    ),
                )

        # for showcase in self.showcases:
        #     self.define_location(
        #         f"Buy {showcase}",
        #         category="Showcases",
        #     )

        # for barrel in self.barrels:
        #     self.define_location(
        #         f"Buy {barrel}",
        #         category="Barrels",
        #     )

        # for slime_pot_index in range(5):
        #     self.define_location(
        #         f"Buy Slime Pot {slime_pot_index + 1}",
        #         category="Slime Pots",
        #     )


spec = PotionomicsWorldSpec()
