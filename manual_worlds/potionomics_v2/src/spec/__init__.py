from dataclasses import dataclass

from .requires import Requires
from .world import WorldSpec


spec = WorldSpec()

chapter_count = 5


def __get_chapter_region_name(chapter_number: int):
    return f"Chapter {chapter_number}"


def __chapter_numbers():
    return range(1, chapter_count + 1)


license = spec.define_item(
    "Progressive License",
    category="Progression",
    progression=True,
    count=chapter_count,
    starting_count=1,
)

contest_reward = spec.define_item(
    "Contest Reward",
    category="Progression",
    progression_skip_balancing=True,
    count=chapter_count,
)

for chapter_number in __chapter_numbers():
    chapter_requirement = Requires.item(license, chapter_number)

    (_, chapter_region) = spec.define_region(
        __get_chapter_region_name(chapter_number),
        starting=True,
        requires=Requires.all_of(
            Requires.item(license, chapter_number),
            Requires.item(contest_reward, chapter_number - 1),
        ),
    )

    if chapter_number < chapter_count:
        chapter_region["connects_to"] = [__get_chapter_region_name(chapter_number + 1)]

    contest_location = spec.define_location(
        f"Win Contest {chapter_number}",
        category=["Contests", f"Chapter {chapter_number}"],
        region=__get_chapter_region_name(chapter_number),
        requires=Requires.all_of(
            Requires.item("Mint"),
            Requires.item("Quinn"),
            Requires.item("Muktuk"),
        ),
    )

spec.define_location(
    "Save the Shop",
    category="Victory",
    requires=Requires.item(contest_reward, "all"),
    victory=True,
)


# region characters/cards
@dataclass
class CardSpec:
    rank: int


@dataclass
class CharacterSpec:
    name: str
    chapter: int
    cards: dict[str, CardSpec]


characters = {
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

for character_name, character_spec in characters.items():
    character_item = spec.define_item(
        character_name,
        category="Characters",
        progression=True,
    )

    if character_name in ["Quinn", "Mint", "Muktuk"]:
        character_item["early"] = True

    spec.define_item(
        f"{character_name} - Progressive Cards",
        category="Cards",
        useful=True,
        count=len(character_spec.cards),
    )

    spec.define_location(
        f"Hang Out with {character_name}",
        category=[
            f"Hang Out",
            f"Chapter {character_spec.chapter}",
        ],
        region=__get_chapter_region_name(character_spec.chapter),
        requires=Requires.item(character_item),
    )

    spec.define_location(
        f"Give {character_name} a Gift",
        category=[
            f"Gift",
            f"Chapter {character_spec.chapter}",
        ],
        region=__get_chapter_region_name(character_spec.chapter),
        requires=Requires.item(character_item),
    )

    spec.define_location(
        f"Accept {character_name}'s Confession",
        category=[f"Confessions"],
        region=__get_chapter_region_name(character_spec.chapter),
        requires=Requires.item(character_item),
        prehint=True,
    )
# endregion characters/cards


# region cauldrons
@dataclass
class CauldronSpec:
    chapter: int
    max_magimins: int


cauldrons: dict[str, CauldronSpec] = {
    # starters
    # "Wooden Cauldron": CauldronSpec(chapter=1, max_magimins=75),
    # "Clay Cauldron": CauldronSpec(chapter=1, max_magimins=115),
    # chapter 1
    "Mudpack Cauldron": CauldronSpec(chapter=1, max_magimins=225),
    "Glass Cauldron": CauldronSpec(chapter=1, max_magimins=200),
    # chapter 2
    "Storm Cauldron": CauldronSpec(chapter=2, max_magimins=375),
    "Ocean Cauldron": CauldronSpec(chapter=2, max_magimins=320),
    "Shadow Cauldron": CauldronSpec(chapter=2, max_magimins=345),
    # chapter 3
    "Crystal Cauldron": CauldronSpec(chapter=3, max_magimins=575),
    "Steel Cauldron": CauldronSpec(chapter=3, max_magimins=540),
    "Celestial Cauldron": CauldronSpec(chapter=3, max_magimins=505),
    # chapter 4
    "Arctic Cauldron": CauldronSpec(chapter=4, max_magimins=975),
    "Crater Cauldron": CauldronSpec(chapter=4, max_magimins=940),
    "Dragon Cauldron": CauldronSpec(chapter=4, max_magimins=860),
    # chapter 5
    "Magical Wasteland Cauldron": CauldronSpec(chapter=5, max_magimins=2000),
}


progressive_cauldrons = spec.define_item(
    f"Progressive Cauldrons",
    category=f"Cauldrons",
    progression=True,
    count=chapter_count,
    starting_count=1,
    early=1,
)

for cauldron, cauldron_spec in cauldrons.items():
    spec.define_location(
        f"Buy a {cauldron}",
        category=[
            f"Cauldrons",
            f"Chapter {cauldron_spec.chapter}",
        ],
        region=__get_chapter_region_name(cauldron_spec.chapter),
        requires=Requires.all_of(
            Requires.item("Muktuk"),
            Requires.item(progressive_cauldrons, cauldron_spec.chapter),
        ),
    )
# endregion cauldrons


# region potions
@dataclass
class PotionSpec:
    chapter: int


potions = {
    "Health Potion": PotionSpec(chapter=1),
    "Mana Potion": PotionSpec(chapter=1),
    "Stamina Potion": PotionSpec(chapter=2),
    "Speed Potion": PotionSpec(chapter=2),
    "Tolerance Potion": PotionSpec(chapter=4),
    "Fire Tonic": PotionSpec(chapter=1),
    "Ice Tonic": PotionSpec(chapter=2),
    "Thunder Tonic": PotionSpec(chapter=2),
    "Shadow Tonic": PotionSpec(chapter=2),
    "Radiation Tonic": PotionSpec(chapter=4),
    "Sight Enhancer": PotionSpec(chapter=1),
    "Alertness Enhancer": PotionSpec(chapter=2),
    "Insight Enhancer": PotionSpec(chapter=3),
    "Dowsing Enhancer": PotionSpec(chapter=3),
    "Seeking Enhancer": PotionSpec(chapter=4),
    "Poison Cure": PotionSpec(chapter=1),
    "Drowsiness Cure": PotionSpec(chapter=2),
    "Petrification Cure": PotionSpec(chapter=3),
    "Silence Cure": PotionSpec(chapter=3),
    "Curse Cure": PotionSpec(chapter=4),
}

for potion, potion_spec in potions.items():
    potion_location = spec.define_location(
        f"Brew {potion}",
        category=[f"Potions", f"Chapter {potion_spec.chapter}"],
        region=__get_chapter_region_name(potion_spec.chapter),
    )

    # past the initial few starter potions,
    # you need certain key characters to feasibly make anything else
    if potion not in ["Health Potion", "Mana Potion", "Fire Tonic"]:
        potion_location["requires"] = Requires.all_of(
            Requires.item("Quinn"),
            Requires.item("Muktuk"),
        )
# endregion potions


# region potion tiers
@dataclass
class PotionTierSpec:
    chapter: int
    magimin_requirements: tuple[int, int, int, int, int, int]
    """The amount of magimins required for each star rating in this tier, from 0 to 5"""


potion_tiers = {
    "Minor": PotionTierSpec(chapter=1, magimin_requirements=(0, 10, 20, 30, 40, 50)),
    "Common": PotionTierSpec(
        chapter=1, magimin_requirements=(60, 75, 90, 105, 115, 130)
    ),
    "Greater": PotionTierSpec(
        chapter=1, magimin_requirements=(150, 170, 195, 215, 235, 260)
    ),
    "Grand": PotionTierSpec(
        chapter=2, magimin_requirements=(290, 315, 345, 370, 400, 430)
    ),
    "Superior": PotionTierSpec(
        chapter=3, magimin_requirements=(470, 505, 545, 580, 620, 660)
    ),
    "Masterwork": PotionTierSpec(
        chapter=4, magimin_requirements=(720, 800, 875, 960, 1040, 1121)
    ),
}

for potion_tier, potion_tier_spec in potion_tiers.items():
    potion_tier_requirement = Requires.item(
        progressive_cauldrons, potion_tier_spec.chapter
    )

    if potion_tier not in ["Minor", "Common"]:
        potion_tier_requirement = Requires.all_of(
            potion_tier_requirement,
            Requires.item("Muktuk"),
        )

    spec.define_location(
        f"Brew a {potion_tier} Tier Potion",
        category=["Potions", f"Chapter {potion_tier_spec.chapter}"],
        region=__get_chapter_region_name(potion_tier_spec.chapter),
        requires=potion_tier_requirement,
    )
# endregion potion tiers


# region adventure
@dataclass
class AdventureLocationSpec:
    chapter: int


adventure_locations = {
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

for adventure_location, adventure_location_spec in adventure_locations.items():
    spec.define_location(
        f"Adventure in {adventure_location}",
        category=[f"Adventure", f"Chapter {adventure_location_spec.chapter}"],
        region=__get_chapter_region_name(adventure_location_spec.chapter),
        requires=Requires.any_of(
            Requires.item("Mint"),
            Requires.all_of(Requires.item("Xidriel"), Requires.item(license, 2)),
            Requires.all_of(Requires.item("Corsac"), Requires.item(license, 3)),
        ),
    )
# endregion adventure


# region shop upgrades
@dataclass
class ShopUpgradeSpec:
    upgrade_count: int


shop_upgrades = {
    "Shop Front": ShopUpgradeSpec(upgrade_count=3),
    "Brewing Area": ShopUpgradeSpec(upgrade_count=3),
    "Basement": ShopUpgradeSpec(upgrade_count=3),
}

for shop_upgrade, shop_upgrade_spec in shop_upgrades.items():
    shop_upgrade_item = spec.define_item(
        f"{shop_upgrade} Upgrades",
        category="Shop Upgrades",
        progression=True,
    )

    for shop_upgrade_index in range(shop_upgrade_spec.upgrade_count):
        spec.define_location(
            f"Buy Level {shop_upgrade_index + 2} {shop_upgrade}",
            category=["Shop Upgrades", f"Chapter {shop_upgrade_index + 2}"],
            region=__get_chapter_region_name(shop_upgrade_index + 2),
            requires=Requires.all_of(
                Requires.item(shop_upgrade_item),
                Requires.item("Saffron"),
            ),
            # Basement is very out of the way and unnecessary,
            # so prehint to know if I need to care about it
            prehint=shop_upgrade == "Basement",
        )
# endregion shop upgrades


# region shelves
@dataclass
class ShelfSpec:
    chapter: int


shelves = {
    "Mushroom Mire Shelf": ShelfSpec(chapter=1),
    "Bone Wastes Shelf": ShelfSpec(chapter=1),
    "Storm Plains Shelf": ShelfSpec(chapter=2),
    "Ocean Coasts Shelf": ShelfSpec(chapter=2),
    "Shadow Steppe Shelf": ShelfSpec(chapter=2),
    "Sulfuric Falls Shelf": ShelfSpec(chapter=3),
    "Crystalline Forest Shelf": ShelfSpec(chapter=3),
    "Ice Craggs Shelf": ShelfSpec(chapter=3),
    "Crater Shelf": ShelfSpec(chapter=4),
    "Dragon Oasis Shelf": ShelfSpec(chapter=4),
    "Arctic Shelf": ShelfSpec(chapter=4),
    "Magical Wasteland Shelf": ShelfSpec(chapter=5),
}

for shelf_name, shelf_spec in shelves.items():
    spec.define_location(
        f"Buy a {shelf_name}",
        category=["Shelves", f"Chapter {shelf_spec.chapter}"],
        region=__get_chapter_region_name(shelf_spec.chapter),
        requires=Requires.item("Muktuk"),
        prehint=True,
    )
# endregion shelves


# region showcases
@dataclass
class ShowcaseSpec:
    chapter: int


showcases = {
    # chapter 1
    "Mushroom Mire Showcase": ShowcaseSpec(chapter=1),
    "Bone Wastes Showcase": ShowcaseSpec(chapter=1),
    # chapter 2
    "Storm Plains Showcase": ShowcaseSpec(chapter=2),
    "Ocean Coasts Showcase": ShowcaseSpec(chapter=2),
    "Shadow Steppe Showcase": ShowcaseSpec(chapter=2),
    # chapter 3
    "Sulfuric Falls Showcase": ShowcaseSpec(chapter=3),
    "Crystalline Forest Showcase": ShowcaseSpec(chapter=3),
    "Ice Craggs Showcase": ShowcaseSpec(chapter=3),
    # chapter 4
    "Crater Showcase": ShowcaseSpec(chapter=4),
    "Dragon Oasis Showcase": ShowcaseSpec(chapter=4),
    "Arctic Showcase": ShowcaseSpec(chapter=4),
    # chapter 5
    "Magical Wasteland Showcase": ShowcaseSpec(chapter=5),
}

for showcase_name, showcase_spec in showcases.items():
    spec.define_location(
        f"Buy a {showcase_name}",
        category=["Showcases", f"Chapter {showcase_spec.chapter}"],
        region=__get_chapter_region_name(showcase_spec.chapter),
        requires=Requires.item("Muktuk"),
        prehint=True,
    )
# endregion showcases
