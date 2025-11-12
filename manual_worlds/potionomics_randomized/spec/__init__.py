from ..lib.world import ItemData, WorldSpec
from ..lib.requires import Requires


class TemplateWorldSpec(WorldSpec):
    def __init__(self):
        super().__init__(
            game="PotionomicsRandomized",
            creator="MapleLeaf",
            filler_item_name="One (1) Gold Coin",
        )

        victory_item = self.define_item(
            "Progressive Will to Persist",
            category="Victory",
            progression=True,
            count=10,
        )

        self.define_location(
            "Just Another Day at the Shop",
            victory=True,
            requires=Requires.item(victory_item, "70%"),
        )

        progressive_cauldrons_item = self.define_item(
            "Progressive Cauldrons",
            category="Cauldrons",
            classification_count={
                "progression + useful": 5,
                "progression": 3,
            },
        )

        recipes_category = self.define_category("Recipes", starting_count=1)[0]

        def define_recipe_item(name: str):
            return self.define_item(
                name,
                category=recipes_category,
                progression=True,
            )

        potion_recipes_item = define_recipe_item("Potion Recipes")
        tonic_recipes_item = define_recipe_item("Tonic Recipes")
        enhancer_recipes_item = define_recipe_item("Enhancer Recipes")
        cure_recipes_item = define_recipe_item("Cure Recipes")

        def define_potion(potion_name: str, recipe_item: ItemData):
            self.define_location(
                f"Brew {potion_name}",
                category=[f"Potions - {recipe_item['name']}"],
                requires=Requires.item(recipe_item),
            )

        define_potion("Health Potion", potion_recipes_item)
        define_potion("Mana Potion", potion_recipes_item)
        define_potion("Stamina Potion", potion_recipes_item)
        define_potion("Speed Potion", potion_recipes_item)
        define_potion("Tolerance Potion", potion_recipes_item)

        define_potion("Fire Tonic", tonic_recipes_item)
        define_potion("Ice Tonic", tonic_recipes_item)
        define_potion("Thunder Tonic", tonic_recipes_item)
        define_potion("Shadow Tonic", tonic_recipes_item)
        define_potion("Radiation Tonic", tonic_recipes_item)

        define_potion("Sight Enhancer", enhancer_recipes_item)
        define_potion("Alertness Enhancer", enhancer_recipes_item)
        define_potion("Insight Enhancer", enhancer_recipes_item)
        define_potion("Dowsing Enhancer", enhancer_recipes_item)
        define_potion("Seeking Enhancer", enhancer_recipes_item)

        define_potion("Poison Cure", cure_recipes_item)
        define_potion("Drowsiness Cure", cure_recipes_item)
        define_potion("Petrification Cure", cure_recipes_item)
        define_potion("Silence Cure", cure_recipes_item)
        define_potion("Curse Cure", cure_recipes_item)

        def define_potion_quality(
            quality_name: str,
            required_progressive_cauldron_count: int,
        ):
            self.define_location(
                f"Brew a {quality_name} Quality Potion",
                category="Potion Qualities",
                requires=Requires.item(
                    progressive_cauldrons_item, required_progressive_cauldron_count
                ),
            )

        define_potion_quality("Minor", 0)
        define_potion_quality("Common", 0)
        define_potion_quality("Greater", 1)
        define_potion_quality("Grand", 2)
        define_potion_quality("Superior", 2)
        define_potion_quality("Masterwork", 3)

        ingredients_category = self.define_category("Ingredients", starting_count=1)[0]

        def define_ingredient_type(name: str):
            self.define_item(
                f"{name} Ingredients",
                category=ingredients_category,
                classification_count={"useful": 1, "filler": 1},
            )

        define_ingredient_type("Bone")
        define_ingredient_type("Bug")
        define_ingredient_type("Essence")
        define_ingredient_type("Fish")
        define_ingredient_type("Flesh")
        define_ingredient_type("Flower")
        define_ingredient_type("Fruit")
        define_ingredient_type("Fungus")
        define_ingredient_type("Gem")
        define_ingredient_type("Mineral")
        define_ingredient_type("Ore")
        define_ingredient_type("Plant")
        define_ingredient_type("Pure Mana")
        define_ingredient_type("Slime")

        characters_category = self.define_category(
            "Characters",
            starting_count=1,
        )[0]

        def define_character(
            character_name: str, additional_locations: list[str] | None = None
        ):
            character_item = self.define_item(
                character_name,
                category=characters_category,
                progression=True,
                useful=True,
            )

            # self.define_item(
            #     f"Progessive Cards - {character_name}",
            #     category="Cards",
            #     classification_count={"useful": 5, "filler": 3},
            # )

            self.define_location(
                f"Hang Out with {character_name}",
                category=f"Characters - {character_name}",
                requires=Requires.item(character_item),
            )

            self.define_location(
                f"Give {character_name} a Gift",
                category=f"Characters - {character_name}",
                requires=Requires.item(character_item),
            )

            for additional_location_name in additional_locations or []:
                self.define_location(
                    additional_location_name,
                    category=f"Characters - {character_name}",
                    requires=Requires.item(character_item),
                )

            return character_item

        define_character("Quinn")
        mint = define_character("Mint", additional_locations=["Adventure with Mint"])
        define_character(
            "Baptiste", additional_locations=["Make an Investment with Baptiste"]
        )
        define_character("Muktuk")
        define_character("Saffron")
        define_character(
            "Roxanne", additional_locations=["Buy an Enchantment from Roxanne"]
        )
        xidriel = define_character(
            "Xidriel", additional_locations=["Adventure with Xidriel"]
        )
        define_character(
            "Salt & Pepper", additional_locations=["Buy a Chest from Salt & Pepper"]
        )
        corsac = define_character(
            "Corsac", additional_locations=["Adventure with Corsac"]
        )
        define_character("Luna", additional_locations=["Start a Campaign with Luna"])
        define_character("Finn")

        adventure_category = self.define_category(
            "Adventure",
            starting_count=1,
        )[0]

        def define_adventure_region(number: int):
            return self.define_item(
                f"Adventure Region {number}",
                category=adventure_category,
                progression=True,
            )

        adventure_region_1 = define_adventure_region(1)
        adventure_region_2 = define_adventure_region(2)
        adventure_region_3 = define_adventure_region(3)
        adventure_region_4 = define_adventure_region(4)
        adventure_region_5 = define_adventure_region(5)

        def define_adventure_location(
            adventure_location_name: str, adventure_region: ItemData
        ):
            self.define_location(
                f"Adventure in {adventure_location_name}",
                category=adventure_region["name"],
                requires=Requires.all_of(
                    adventure_region, Requires.any_of(mint, xidriel, corsac)
                ),
            )

        define_adventure_location("Enchanted Forest", adventure_region_1)
        define_adventure_location("Bone Wastes", adventure_region_1)
        define_adventure_location("Mushroom Mire", adventure_region_1)

        define_adventure_location("Shadow Steppe", adventure_region_2)
        define_adventure_location("Ocean Coasts", adventure_region_2)
        define_adventure_location("Storm Plains", adventure_region_2)

        define_adventure_location("Sulfuric Falls", adventure_region_3)
        define_adventure_location("Crystalline Forest", adventure_region_3)
        define_adventure_location("Ice Craggs", adventure_region_3)

        define_adventure_location("Dragon Oasis", adventure_region_4)
        define_adventure_location("Crater", adventure_region_4)
        define_adventure_location("Arctic", adventure_region_4)

        define_adventure_location("Magical Wasteland", adventure_region_5)

        self.define_item(
            "Cauldron Slot",
            category="Enhancements",
            classification_count={"useful": 3, "filler": 3},
            starting_count=1,
        )

        self.define_item(
            "Vending Machine Slot",
            category="Enhancements",
            classification_count={"useful": 8, "filler": 4},
        )

        self.define_item(
            "Store Shelf Slot",
            category="Enhancements",
            classification_count={"useful": 4, "filler": 2},
            starting_count=1,
        )

        self.define_item(
            "Showcase Slot",
            category="Enhancements",
            classification_count={"useful": 3, "filler": 1},
        )


world_spec = TemplateWorldSpec()
