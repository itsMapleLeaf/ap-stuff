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

    ingredients: ClassVar[dict[str, IngredientSpec]] = {}
    for ingredient_data in cast(
        list[dict], load_data_file("potionomics_ingredients.json")
    ):
        ingredients[str(ingredient_data["name"])] = IngredientSpec(**ingredient_data)

    ingredient_types: ClassVar = {
        # TODO: use data that doesn't have null values for these
        ingredient.type
        for ingredient in ingredients.values()
        if ingredient.type != None
    }

    ingredient_rarities: ClassVar = {
        # TODO: use data that doesn't have null values for these
        ingredient.rarity
        for ingredient in ingredients.values()
        if ingredient.rarity != None
    }

    @dataclass
    class PotionSpec:
        level: int

    potions: ClassVar = {
        "Health Potion": PotionSpec(level=1),
        "Mana Potion": PotionSpec(level=1),
        "Stamina Potion": PotionSpec(level=2),
        "Speed Potion": PotionSpec(level=2),
        "Tolerance Potion": PotionSpec(level=4),
        "Fire Tonic": PotionSpec(level=1),
        "Ice Tonic": PotionSpec(level=2),
        "Thunder Tonic": PotionSpec(level=2),
        "Shadow Tonic": PotionSpec(level=2),
        "Radiation Tonic": PotionSpec(level=4),
        "Sight Enhancer": PotionSpec(level=1),
        "Alertness Enhancer": PotionSpec(level=2),
        "Insight Enhancer": PotionSpec(level=3),
        "Dowsing Enhancer": PotionSpec(level=3),
        "Seeking Enhancer": PotionSpec(level=4),
        "Poison Cure": PotionSpec(level=1),
        "Drowsiness Cure": PotionSpec(level=2),
        "Petrification Cure": PotionSpec(level=3),
        "Silence Cure": PotionSpec(level=3),
        "Curse Cure": PotionSpec(level=4),
    }

    @dataclass
    class PotionTierSpec:
        magimin_requirements: tuple[int, int, int, int, int, int]
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
        max_magimins: int

    cauldrons: ClassVar[dict[str, CauldronSpec]] = {
        "Wooden Cauldron": CauldronSpec(max_magimins=75),
        "Clay Cauldron": CauldronSpec(max_magimins=115),
        "Mudpack Cauldron": CauldronSpec(max_magimins=225),
        "Glass Cauldron": CauldronSpec(max_magimins=200),
        "Storm Cauldron": CauldronSpec(max_magimins=375),
        "Ocean Cauldron": CauldronSpec(max_magimins=320),
        "Shadow Cauldron": CauldronSpec(max_magimins=345),
        "Crystal Cauldron": CauldronSpec(max_magimins=575),
        "Steel Cauldron": CauldronSpec(max_magimins=540),
        "Celestial Cauldron": CauldronSpec(max_magimins=505),
        "Arctic Cauldron": CauldronSpec(max_magimins=975),
        "Crater Cauldron": CauldronSpec(max_magimins=940),
        "Dragon Cauldron": CauldronSpec(max_magimins=860),
        "Magical Wasteland Cauldron": CauldronSpec(max_magimins=2000),
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
        # ingredient_types_category = "Ingredient Types"
        # ingredient_rarities_category = "Ingredient Rarities"
        adventure_locations_category = "Adventure Locations"

        starting_adventure_locations = [
            f"Map to {location}"
            for location, spec in self.adventure_locations.items()
            if spec.chapter == 1
        ]

        super().__init__(
            starting_items=[
                {"items": ["License Level+"], "random": 1},
                {"item_categories": ["Level 1 Recipes"], "random": 3},
                # {"items": ["Wooden Cauldron"], "random": 1},
                # {"items": ["Magimin Limit +10"], "random": 1},
                {"item_categories": ["Cards"], "random": 5},
                {"items": starting_adventure_locations},
            ]
        )

        potion_completion = self.define_item(
            "Potion Completion",
            category="Completion",
            progression=True,
            count=len(self.potions),
        )

        romance_completion_item = self.define_item(
            "Find the Love of your Life",
            category="Completion",
            progression=True,
        )

        self.define_location(
            "Find the Love of your Life",
            category="Completion",
            place_item=[romance_completion_item["name"]],
        )

        self.define_location(
            "Potion Master",
            requires=(
                f"|{potion_completion['name']}:50%|"
                f" and |{romance_completion_item['name']}:all|"
            ),
            category="Completion",
            victory=True,
        )

        # region licenses
        license_level_item = self.define_item(
            "License Level+",
            category="Licenses",
            progression=True,
            count=4,
        )

        for license_level in (2, 3, 4):
            self.define_location(
                f"Obtain Level {license_level} License",
                category="Licenses",
                requires=f"|{license_level_item['name']}:{license_level - 1}|",
                place_item=[license_level_item["name"]],
            )
        # endregion licenses

        # region magimin limit
        # magimin_limit_item = self.define_item(
        #     "Magimin Limit +10",
        #     category="Magimin Limit",
        #     count=200 // 10,
        #     progression=True,
        # )
        # endregion magimin limit

        # region potions
        for potion_name, potion_spec in self.potions.items():
            potion_recipe_item = self.define_item(
                f"{potion_name} Recipe",
                category=["Potion Recipes", f"Level {potion_spec.level} Recipes"],
                progression=True,
            )

            self.define_location(
                f"Brew {potion_name}",
                category=f"Potions - {potion_name}",
                requires=(
                    f"|{potion_recipe_item['name']}|"
                    f" and |{license_level_item['name']}:{potion_spec.level}|"
                ),
                place_item=[potion_completion["name"]],
            )

            for potion_tier, potion_tier_spec in [*self.potion_tiers.items()][1:]:
                self.define_location(
                    f"Brew {potion_tier} {potion_name} or higher",
                    category=f"Potions - {potion_name}",
                    requires=(
                        f"|{potion_recipe_item['name']}|"
                        f" and |{license_level_item['name']}:{potion_spec.level}|"
                        # f" and |@Can Brew {potion_tier}|"
                        # f" and |{magimin_limit_item['name']}:{potion_tier_spec.magimin_requirements[0] // 10 // 10}|"
                    ),
                )
        # endregion potions

        # region ingredients
        # for ingredient_type in self.ingredient_types:
        #     self.define_item(
        #         f"{ingredient_type} Ingredients",
        #         category=ingredient_types_category,
        #         progression=True,
        #     )

        # for ingredient_rarity in self.ingredient_rarities:
        #     self.define_item(
        #         f"{ingredient_rarity} Ingredients",
        #         category=ingredient_rarities_category,
        #         progression=True,
        #     )
        # endregion ingredients

        # region adventure
        for (
            adventure_location,
            adventure_location_spec,
        ) in self.adventure_locations.items():
            adventure_location_item = self.define_item(
                f"Map to {adventure_location}",
                category=adventure_locations_category,
                progression=True,
            )

            self.define_location(
                f"Adventure in {adventure_location}",
                category=adventure_locations_category,
                requires=(
                    f"|{adventure_location_item['name']}|"
                    f" and |{license_level_item['name']}:{adventure_location_spec.chapter - 1}|"
                ),
            )
        # endregion adventure

        # region characters/cards
        for character_name, character_spec in self.characters.items():
            self.define_item(
                f"Cards ({character_name})",
                category=["Cards"],
                useful=True,
                count=len(character_spec.cards),
            )

            # for character_rank in range(10):
            #     self.define_location(
            #         (
            #             f"Meet {character_name}"
            #             if character_rank_index == 0
            #             else f"{character_name} - Reach Rank {character_rank_index + 1}"
            #         ),
            #         category=[f"Characters - {character_name}"],
            #         requires=f"|{license_level_item['name']}:{character_spec.chapter}|",
            #     )
        # endregion characters/cards

        # region cauldrons
        # for cauldron_name, cauldron_spec in self.cauldrons.items():
        #     self.define_item(
        #         cauldron_name,
        #         category=[
        #             "Cauldrons",
        #             *(
        #                 f"Can Brew {tier}"
        #                 for tier, tier_spec in self.potion_tiers.items()
        #                 if (
        #                     cauldron_spec.max_magimins
        #                     > tier_spec.magimin_requirements[0]
        #                 )
        #             ),
        #         ],
        #         progression=True,
        #     )
        # endregion cauldrons


spec = PotionomicsWorldSpec()
