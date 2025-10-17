from typing import Optional
from .world import WorldSpec
from .requires import Requires


def __define_world_spec() -> WorldSpec:
    spec = WorldSpec()

    day_1 = "Chapter 1 - Day 1"
    day_2 = "Chapter 1 - Day 2"
    day_3 = "Chapter 1 - Day 3"

    chapter_1 = "Chapter 1"
    chapter_2 = "Chapter 2"
    chapter_3 = "Chapter 3"
    chapter_4 = "Chapter 4"
    chapter_5 = "Chapter 5"

    license_level = spec.define_item(
        "Progressive License Level",
        category="Progression",
        progression=True,
        count=5,
        starting_count=1,
    )["name"]

    contest_reward = spec.define_item(
        "Contest Reward",
        category="Contest Rewards",
        progression=True,
        count=5,
    )["name"]

    spec.define_location(
        "Save the Shop!",
        category="Victory",
        region=chapter_5,
        requires=Requires.item(contest_reward, "all"),
        victory=True,
    )

    # region days
    for chapter_index, chapter_region in enumerate(
        [chapter_1, chapter_2, chapter_3, chapter_4, chapter_5]
    ):
        # make locations for days 1-9 of each chapter
        for day in range(1, 10):
            spec.define_location(
                f"Complete Day {chapter_index * 10 + day}",
                category=[chapter_region, "Day Completion"],
                region=chapter_region,
            )
    # endregion days

    # region potions
    potion_recipes_category = "Recipes"

    def define_potion(
        potion_name: str, region: str, recipe_starting_count: Optional[int] = None
    ):
        recipe_item = spec.define_item(
            f"{potion_name} Recipe",
            category=potion_recipes_category,
            progression=True,
            starting_count=recipe_starting_count,
        )

        spec.define_location(
            f"Brew a {potion_name}",
            category=["Potions", region],
            region=region,
            requires=Requires.item(recipe_item),
        )

        return recipe_item["name"]

    health_potion_recipe = define_potion(
        "Health Potion", region=day_1, recipe_starting_count=1
    )
    mana_potion_recipe = define_potion(
        "Mana Potion", region=day_1, recipe_starting_count=1
    )
    stamina_potion_recipe = define_potion("Stamina Potion", region=chapter_2)
    speed_potion_recipe = define_potion("Speed Potion", region=chapter_2)
    tolerance_potion_recipe = define_potion("Tolerance Potion", region=chapter_4)

    fire_tonic_recipe = define_potion("Fire Tonic", region=day_2)
    ice_tonic_recipe = define_potion("Ice Tonic", region=chapter_2)
    thunder_tonic_recipe = define_potion("Thunder Tonic", region=chapter_2)
    shadow_tonic_recipe = define_potion("Shadow Tonic", region=chapter_2)
    radiation_tonic_recipe = define_potion("Radiation Tonic", region=chapter_4)

    sight_enhancer_recipe = define_potion("Sight Enhancer", region=chapter_1)
    alertness_enhancer_recipe = define_potion("Alertness Enhancer", region=chapter_2)
    insight_enhancer_recipe = define_potion("Insight Enhancer", region=chapter_3)
    dowsing_enhancer_recipe = define_potion("Dowsing Enhancer", region=chapter_3)
    seeking_enhancer_recipe = define_potion("Seeking Enhancer", region=chapter_4)

    poison_cure_recipe = define_potion("Poison Cure", region=chapter_1)
    drowsiness_cure_recipe = define_potion("Drowsiness Cure", region=chapter_2)
    petrification_cure_recipe = define_potion("Petrification Cure", region=chapter_3)
    silence_cure_recipe = define_potion("Silence Cure", region=chapter_3)
    curse_cure_recipe = define_potion("Curse Cure", region=chapter_4)

    def define_potion_quality(quality_name: str, region: str):
        spec.define_location(
            f"Brew a {quality_name} Potion",
            category=["Potions", region],
            region=region,
            requires=Requires.category(potion_recipes_category),
        )

    define_potion_quality("Minor", region=day_1)
    define_potion_quality("Common", region=chapter_1)
    define_potion_quality("Greater", region=chapter_2)
    define_potion_quality("Grand", region=chapter_3)
    define_potion_quality("Superior", region=chapter_4)
    define_potion_quality("Masterwork", region=chapter_5)
    # endregion potions

    # region characters
    characters_item_category = "Characters"

    def define_character(
        character_name: str,
        region: str,
        starting_count: int | None = None,
        early: bool = False,
    ):
        character_item = spec.define_item(
            character_name,
            category=[characters_item_category],
            progression=True,
            starting_count=starting_count,
            early=early,
        )

        spec.define_item(
            f"{character_name} (Progressive Cards)",
            category=["Cards"],
            useful=True,
            count=10,
        )

        spec.define_location(
            f"Hang Out with {character_name}",
            category=[character_name, region],
            region=region,
            requires=Requires.item(character_item),
        )

        spec.define_location(
            f"Rank Up {character_name}",
            category=[character_name, region],
            region=region,
            requires=Requires.item(character_item),
        )

        spec.define_location(
            f"Give a Gift to {character_name}",
            category=[character_name, region],
            region=region,
            requires=Requires.item(character_item),
        )

        spec.define_location(
            f"Accept {character_name}'s Confession",
            category=["Confessions"],
            requires=Requires.item(character_item),
            # it's effectively impossible to level them up before chapter 4,
            # but if you _somehow_ do, then that can be a valid logic break
            region=chapter_4,
            # this is difficult and basically optional in the base game,
            # so prehint so we know if it's needed
            prehint=True,
        )

        return character_name

    quinn = define_character("Quinn", region=day_2, starting_count=1)
    mint = define_character("Mint", region=day_2, early=True)
    muktuk = define_character("Muktuk", region=day_3)
    baptiste = define_character("Baptiste", region=chapter_1)
    saffron = define_character("Saffron", region=chapter_1)
    roxanne = define_character("Roxanne", region=chapter_2)
    xidriel = define_character("Xidriel", region=chapter_2)
    luna = define_character("Luna", region=chapter_3)
    salt_and_pepper = define_character("Salt & Pepper", region=chapter_3)
    corsac = define_character("Corsac", region=chapter_4)
    # finn = define_character("Finn", region=chapter_4)
    # endregion characters

    # region cauldrons
    # defines which cauldrons you can access
    # amount you have = each cauldron's respective chapter level
    # e.g. with 3, you can access chapter 1, 2, and 3 cauldrons
    progressive_cauldrons = spec.define_item(
        "Progressive Cauldrons",
        category=["Progression"],
        progression=True,
        count=5,
        starting_count=1,
    )["name"]

    def define_cauldron(cauldron_name: str, region: str, level: int):
        for i in range(3):
            spec.define_location(
                i == 0
                and f"Buy a {cauldron_name} Cauldron"
                or f"Upgrade to {cauldron_name} Cauldron{"+" * i}",
                category=["Cauldrons", region],
                region=region,
                requires=Requires.all_of(
                    Requires.item(muktuk), Requires.item(progressive_cauldrons, level)
                ),
            )

    define_cauldron("Mudpack", region=chapter_1, level=1)
    define_cauldron("Glass", region=chapter_1, level=1)

    define_cauldron("Storm", region=chapter_2, level=2)
    define_cauldron("Ocean", region=chapter_2, level=2)
    define_cauldron("Shadow", region=chapter_2, level=2)

    define_cauldron("Crystal", region=chapter_3, level=3)
    define_cauldron("Steel", region=chapter_3, level=3)
    define_cauldron("Celestial", region=chapter_3, level=3)

    define_cauldron("Arctic", region=chapter_4, level=4)
    define_cauldron("Crater", region=chapter_4, level=4)
    define_cauldron("Dragon", region=chapter_4, level=4)

    define_cauldron("Magical Wasteland", region=chapter_5, level=5)
    # endregion cauldrons

    # region adventure
    def define_adventure_location(
        location_name: str,
        region: str,
        map_starting_count: Optional[int] = None,
        map_early: bool = False,
    ):
        map_item = spec.define_item(
            f"Map to {location_name}",
            category=["Adventure"],
            progression=True,
            starting_count=map_starting_count,
            early=map_early,
        )

        spec.define_location(
            f"Adventure in {location_name}",
            category=["Adventure", region],
            region=region,
            requires=Requires.all_of(Requires.item(map_item), Requires.item(mint)),
        )

        return map_item["name"]

    enchanted_forest_map = define_adventure_location(
        "Enchanted Forest", region=day_2, map_starting_count=1
    )
    bone_wastes_map = define_adventure_location(
        "Bone Wastes", region=chapter_1, map_early=True
    )
    mushroom_mire_map = define_adventure_location("Mushroom Mire", region=chapter_1)

    shadow_steppe_map = define_adventure_location("Shadow Steppe", region=chapter_2)
    ocean_coasts_map = define_adventure_location("Ocean Coasts", region=chapter_2)
    storm_plains_map = define_adventure_location("Storm Plains", region=chapter_2)

    sulfuric_falls_map = define_adventure_location("Sulfuric Falls", region=chapter_3)
    crystalline_forest_map = define_adventure_location(
        "Crystalline Forest", region=chapter_3
    )
    ice_craggs_map = define_adventure_location("Ice Craggs", region=chapter_3)

    dragon_oasis_map = define_adventure_location("Dragon Oasis", region=chapter_4)
    crater_map = define_adventure_location("Crater", region=chapter_4)
    arctic_map = define_adventure_location("Arctic", region=chapter_4)

    magical_wasteland_map = define_adventure_location(
        "Magical Wasteland", region=chapter_5
    )
    # endregion adventure

    # region shop upgrades
    def define_shop_upgrade(
        upgrade_name: str,
        level: int,
        region: str,
    ):
        spec.define_location(
            f"Buy Level {level} {upgrade_name}",
            category=["Shop Upgrades", region],
            region=region,
            requires=Requires.item(saffron),
        )

    define_shop_upgrade("Shop Front", level=2, region=chapter_2)
    define_shop_upgrade("Shop Front", level=3, region=chapter_3)
    define_shop_upgrade("Shop Front", level=4, region=chapter_4)

    define_shop_upgrade("Brewing Area", level=2, region=chapter_2)
    define_shop_upgrade("Brewing Area", level=3, region=chapter_2)
    define_shop_upgrade("Brewing Area", level=4, region=chapter_3)

    define_shop_upgrade("Basement", level=2, region=chapter_2)
    define_shop_upgrade("Basement", level=3, region=chapter_3)
    define_shop_upgrade("Basement", level=4, region=chapter_4)
    # endregion shop upgrades

    # region shelves
    def define_shelf(shelf_name: str, region: str):
        spec.define_location(
            f"Buy a {shelf_name} Shelf",
            category=["Shelves", region],
            region=region,
            requires=Requires.item(muktuk),
        )
        spec.define_location(
            f"Upgrade to {shelf_name} Shelf+",
            category=["Shelves", region],
            region=region,
            requires=Requires.item(muktuk),
        )
        spec.define_location(
            f"Upgrade to {shelf_name} Shelf++",
            category=["Shelves", region],
            region=region,
            requires=Requires.item(muktuk),
        )

    define_shelf("Mushroom Mire", chapter_1)
    define_shelf("Bone Wastes", chapter_1)

    define_shelf("Storm Plains", chapter_2)
    define_shelf("Ocean Coasts", chapter_2)
    define_shelf("Shadow Steppe", chapter_2)

    define_shelf("Sulfuric Falls", chapter_3)
    define_shelf("Crystalline Forest", chapter_3)
    define_shelf("Ice Craggs", chapter_3)

    define_shelf("Crater", chapter_4)
    define_shelf("Dragon Oasis", chapter_4)
    define_shelf("Arctic", chapter_4)

    define_shelf("Magical Wasteland", chapter_5)
    # endregion shelves

    # region showcases
    def define_showcase(showcase_name: str, region: str, prehint: bool = False):
        spec.define_location(
            f"Buy a {showcase_name} Showcase",
            category=["Shelves", region],
            region=region,
            requires=Requires.item(muktuk),
            prehint=prehint,
        )

    define_showcase("Mushroom Mire", chapter_1)
    define_showcase("Bone Wastes", chapter_1)

    define_showcase("Storm Plains", chapter_2, prehint=True)
    define_showcase("Ocean Coasts", chapter_2, prehint=True)
    define_showcase("Shadow Steppe", chapter_2, prehint=True)

    define_showcase("Sulfuric Falls", chapter_3, prehint=True)
    define_showcase("Crystalline Forest", chapter_3, prehint=True)
    define_showcase("Ice Craggs", chapter_3, prehint=True)

    define_showcase("Crater", chapter_4, prehint=True)
    define_showcase("Dragon Oasis", chapter_4, prehint=True)
    define_showcase("Arctic", chapter_4, prehint=True)

    define_showcase("Magical Wasteland", chapter_5, prehint=True)
    # endregion showcases

    # region barrels
    def define_barrel(barrel_name: str, region: str):
        spec.define_location(
            f"Buy a {barrel_name} Barrel",
            category=["Shelves", region],
            region=region,
            requires=Requires.item(muktuk),
            prehint=True,  # barrels can be ignored normally, always prehint
        )

    # barrels don't show up until chapter 3, so that's the minimum
    define_barrel("Oak Wood", chapter_3)

    define_barrel("Mushroom", chapter_3)
    define_barrel("Cactus", chapter_3)

    define_barrel("Thunder Log", chapter_3)
    define_barrel("Coral", chapter_3)
    define_barrel("Cocoon", chapter_3)

    define_barrel("Vines", chapter_3)
    define_barrel("Prismatic Thunder", chapter_3)
    define_barrel("Frost Kindling", chapter_3)

    define_barrel("Poly Log", chapter_4)
    define_barrel("Scaly Wood", chapter_4)
    define_barrel("Yeti", chapter_4)

    define_barrel("Empyrean Bud", chapter_5)
    # endregion barrels

    # region slots
    # adding extras for a bunch of these just to make sure they get found at some point

    spec.define_item(
        "Cauldron Slots",
        category="Other",
        useful=True,
        count=8,
        starting_count=1,
        early=2,
    )

    spec.define_item(
        "Vending Machine Slots",
        category="Other",
        useful=True,
        count=20,
        starting_count=2,
    )

    spec.define_item(
        "Shelf Slots",
        category="Other",
        useful=True,
        count=8,
        starting_count=1,
        early=1,
    )

    spec.define_item(
        "Display Case Slots",
        category="Other",
        useful=True,
        count=6,
    )
    # endregion slots

    # region chapter regions
    spec.define_region(day_1, starting=True, connects_to=[day_2])
    spec.define_region(day_2, connects_to=[day_3])
    spec.define_region(day_3, connects_to=[chapter_1])

    spec.define_region(
        chapter_1,
        connects_to=[chapter_2],
        requires=Requires.all_of(
            Requires.item(quinn),
            Requires.item(muktuk),
            Requires.item(mint),
            Requires.item(health_potion_recipe),
            Requires.item(fire_tonic_recipe),
            Requires.item(mana_potion_recipe),
            Requires.item(mana_potion_recipe),
            Requires.item(enchanted_forest_map),
            Requires.item(bone_wastes_map),
        ),
    )

    spec.define_region(
        chapter_2,
        connects_to=[chapter_3],
        requires=Requires.all_of(
            Requires.item(baptiste),
            Requires.item(contest_reward, 1),
            Requires.item(license_level, 2),
            Requires.item(ice_tonic_recipe),
            Requires.item(sight_enhancer_recipe),
            Requires.item(speed_potion_recipe),
            Requires.item(mushroom_mire_map),
            Requires.any_of(
                Requires.item(ocean_coasts_map),
                Requires.item(storm_plains_map),
            ),
        ),
    )

    spec.define_region(
        chapter_3,
        connects_to=[chapter_4],
        requires=Requires.all_of(
            Requires.item(saffron),
            Requires.item(xidriel),
            Requires.item(contest_reward, 2),
            Requires.item(license_level, 3),
            Requires.item(poison_cure_recipe),
            Requires.item(thunder_tonic_recipe),
            Requires.item(stamina_potion_recipe),
            Requires.any_of(
                Requires.item(sulfuric_falls_map),
                Requires.item(crystalline_forest_map),
                Requires.item(ice_craggs_map),
            ),
        ),
    )

    spec.define_region(
        chapter_4,
        connects_to=[chapter_5],
        requires=Requires.all_of(
            Requires.category(characters_item_category, 8),
            Requires.item(contest_reward, 3),
            Requires.item(license_level, 4),
            Requires.item(silence_cure_recipe),
            Requires.item(tolerance_potion_recipe),
            Requires.item(insight_enhancer_recipe),
            Requires.any_of(
                Requires.item(dragon_oasis_map),
                Requires.item(crater_map),
                Requires.item(arctic_map),
            ),
        ),
    )

    spec.define_region(
        chapter_5,
        requires=Requires.all_of(
            Requires.category(characters_item_category, "all"),
            Requires.item(contest_reward, 4),
            Requires.item(license_level, 5),
            Requires.item(radiation_tonic_recipe),
            Requires.item(curse_cure_recipe),
            Requires.item(seeking_enhancer_recipe),
            Requires.item(magical_wasteland_map),
        ),
    )
    # endregion chapter regions

    return spec


spec = __define_world_spec()
