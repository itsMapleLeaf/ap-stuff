from dataclasses import dataclass
from typing import ClassVar, cast

from .types import StartingItemData
from .world import WorldSpec
from ..Helpers import load_data_file


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


@dataclass
class AdventureLocationSpec:
    chapter: int


@dataclass
class CardSpec:
    character: str
    rank: int


@dataclass
class CauldronSpec:
    upgrade_count: int = 0


@dataclass
class ShopUpgradeSpec:
    upgrade_count: int = 0


class PotionomicsWorldSpec(WorldSpec):
    ingredients: ClassVar = {
        item["name"]: IngredientSpec(**item)
        for item in cast(list[dict], load_data_file("potionomics_ingredients.json"))
    }

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

    potion_qualities: ClassVar = [
        "Minor",
        "Common",
        "Greater",
        "Grand",
        "Superior",
        "Masterwork",
    ]

    starting_relationship_rank = 2
    max_relationship_rank = 10
    characters: ClassVar = {
        "Quinn",
        "Mint",
        "Baptiste",
        "Muktuk",
        "Saffron",
        "Roxanne",
        "Xidriel",
        "Salt & Pepper",
        "Corsac",
        "Luna",
    }

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

    cards: ClassVar = {
        # Sylvia
        "Set 'Em Up": CardSpec(character="Sylvia", rank=1),
        "Reel 'Em In": CardSpec(character="Sylvia", rank=2),
        "Close It Out": CardSpec(character="Sylvia", rank=3),
        "Brace Yourself": CardSpec(character="Sylvia", rank=4),
        "Think, Sylvia, Think": CardSpec(character="Sylvia", rank=5),
        # Owl
        "Scheme": CardSpec(character="Owl", rank=1),
        "Two is Better Than One": CardSpec(character="Owl", rank=2),
        "Barrage": CardSpec(character="Owl", rank=3),
        "Mulligan": CardSpec(character="Owl", rank=4),
        "Rattle 'Em Off": CardSpec(character="Owl", rank=5),
        # Quinn
        "Hustle": CardSpec(character="Quinn", rank=1),
        "Take It or Leave It": CardSpec(character="Quinn", rank=2),
        "Shock Factor": CardSpec(character="Quinn", rank=3),
        "Plant the Seed": CardSpec(character="Quinn", rank=4),
        "Press the Attack": CardSpec(character="Quinn", rank=5),
        "Pressure": CardSpec(character="Quinn", rank=6),
        "Fuel the Fire": CardSpec(character="Quinn", rank=7),
        "Compound Interest": CardSpec(character="Quinn", rank=8),
        # Mint
        "Sympathy": CardSpec(character="Mint", rank=1),
        "Keep Your Guard Up": CardSpec(character="Mint", rank=2),
        "Muscle Memory": CardSpec(character="Mint", rank=3),
        "Blitz": CardSpec(character="Mint", rank=5),
        "Eye on the Prize": CardSpec(character="Mint", rank=6),
        "Fortitude": CardSpec(character="Mint", rank=7),
        "Unfazed": CardSpec(character="Mint", rank=9),
        "Keep It Simple": CardSpec(character="Mint", rank=1),
        # Baptiste
        "Captivate": CardSpec(character="Baptiste", rank=1),
        "Build Rapport": CardSpec(character="Baptiste", rank=2),
        "Subvert": CardSpec(character="Baptiste", rank=3),
        "Compromise": CardSpec(character="Baptiste", rank=5),
        "Common Ground": CardSpec(character="Baptiste", rank=6),
        "Strategic Withdrawal": CardSpec(character="Baptiste", rank=7),
        "Emotional Intelligence": CardSpec(character="Baptiste", rank=9),
        "Silver Tongue": CardSpec(character="Baptiste", rank=10),
        # Muk'Tuk
        "Pump Up": CardSpec(character="Muk'Tuk", rank=1),
        "Enthusiasm": CardSpec(character="Muk'Tuk", rank=2),
        "Craftsmanship": CardSpec(character="Muk'Tuk", rank=3),
        "Reinforce": CardSpec(character="Muk'Tuk", rank=4),
        "Bravado": CardSpec(character="Muk'Tuk", rank=5),
        "Zeal": CardSpec(character="Muk'Tuk", rank=7),
        "Artistry": CardSpec(character="Muk'Tuk", rank=9),
        "Conviction": CardSpec(character="Muk'Tuk", rank=10),
        # Saffron
        "Meditate": CardSpec(character="Saffron", rank=1),
        "Guided Thought": CardSpec(character="Saffron", rank=2),
        "Casual Conversation": CardSpec(character="Saffron", rank=3),
        "Deep Connection": CardSpec(character="Saffron", rank=5),
        "Mindfulness": CardSpec(character="Saffron", rank=6),
        "Regulated Breathing": CardSpec(character="Saffron", rank=7),
        "Serenity of Mind": CardSpec(character="Saffron", rank=9),
        "Tranquility": CardSpec(character="Saffron", rank=10),
        # Roxanne
        "Sleight of Hand": CardSpec(character="Roxanne", rank=1),
        "Flattery": CardSpec(character="Roxanne", rank=2),
        "Disarm": CardSpec(character="Roxanne", rank=3),
        "Pander": CardSpec(character="Roxanne", rank=5),
        "Emotional Mindfield": CardSpec(character="Roxanne", rank=6),
        "Chapstick": CardSpec(character="Roxanne", rank=7),
        "Magnetism": CardSpec(character="Roxanne", rank=9),
        "Mass Misdirection": CardSpec(character="Roxanne", rank=10),
        # Xidriel
        "Jingle": CardSpec(character="Xidriel", rank=1),
        "Opening Act": CardSpec(character="Xidriel", rank=2),
        "Chorus": CardSpec(character="Xidriel", rank=3),
        "Improv": CardSpec(character="Xidriel", rank=5),
        "Rhythm": CardSpec(character="Xidriel", rank=6),
        "Throat Spray": CardSpec(character="Xidriel", rank=7),
        "Catchy Tune": CardSpec(character="Xidriel", rank=9),
        "Encore": CardSpec(character="Xidriel", rank=10),
        # Salt & Pepper
        "Strike or Strike Later": CardSpec(character="Salt & Pepper", rank=1),
        "Good Cop, Bad Cop": CardSpec(character="Salt & Pepper", rank=2),
        "Salt or Pepper": CardSpec(character="Salt & Pepper", rank=3),
        "Avast Ye!": CardSpec(character="Salt & Pepper", rank=5),
        "Give No Quarter": CardSpec(character="Salt & Pepper", rank=6),
        "Batten Down the Hatches": CardSpec(character="Salt & Pepper", rank=7),
        "Mental Purrrley": CardSpec(character="Salt & Pepper", rank=9),
        "Carpe Diem": CardSpec(character="Salt & Pepper", rank=10),
        # Corsac
        "Ferocity of the Squirrel": CardSpec(character="Corsac", rank=1),
        "Adapt": CardSpec(character="Corsac", rank=2),
        "Be Prepared": CardSpec(character="Corsac", rank=3),
        "Happy Place": CardSpec(character="Corsac", rank=5),
        "Serenity of the Mollus": CardSpec(character="Corsac", rank=6),
        "Pivot": CardSpec(character="Corsac", rank=7),
        "Mind of the Slime": CardSpec(character="Corsac", rank=9),
        "Lessons from Nature": CardSpec(character="Corsac", rank=10),
        # Luna
        "Elevator Pitch": CardSpec(character="Luna", rank=1),
        "Lean into It": CardSpec(character="Luna", rank=2),
        "Wing It": CardSpec(character="Luna", rank=3),
        "Rehearsed Line": CardSpec(character="Luna", rank=5),
        "Caffeine Rush": CardSpec(character="Luna", rank=6),
        "Dig Deep": CardSpec(character="Luna", rank=7),
        "Subliminal Suggestion": CardSpec(character="Luna", rank=9),
        "Final Push": CardSpec(character="Luna", rank=10),
    }

    banned_cards = [
        "Regulated Breathing",
        "Serenity of Mind",
        "Chorus",
        "Rattle 'Em Off",
    ]
    for banned_card_name in banned_cards:
        cards.pop(banned_card_name)

    cauldrons: ClassVar = {
        "Wooden Cauldron": CauldronSpec(),
        "Clay Cauldron": CauldronSpec(),
        "Mudpack Cauldron": CauldronSpec(upgrade_count=2),
        "Glass Cauldron": CauldronSpec(upgrade_count=2),
        "Storm Cauldron": CauldronSpec(upgrade_count=2),
        "Ocean Cauldron": CauldronSpec(upgrade_count=2),
        "Shadow Cauldron": CauldronSpec(upgrade_count=2),
        "Crystal Cauldron": CauldronSpec(upgrade_count=2),
        "Steel Cauldron": CauldronSpec(upgrade_count=2),
        "Celestial Cauldron": CauldronSpec(upgrade_count=2),
        "Arctic Cauldron": CauldronSpec(upgrade_count=2),
        "Crater Cauldron": CauldronSpec(upgrade_count=2),
        "Dragon Cauldron": CauldronSpec(upgrade_count=2),
        "Magical Wasteland Cauldron": CauldronSpec(upgrade_count=2),
    }

    shelves: ClassVar = {
        "Mushroom Mire Shelf",
        "Bone Wastes Shelf",
        "Storm Plains Shelf",
        "Ocean Coasts Shelf",
        "Shadow Steppe Shelf",
        "Sulfuric Falls Shelf",
        "Crystalline Forest Shelf",
        "Ice Craggs Shelf",
        "Crater Shelf",
        "Dragon Oasis Shelf",
        "Arctic Shelf",
        "Magical Wasteland Shelf",
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

    shop_upgrades: ClassVar = {
        "Shop Front": ShopUpgradeSpec(upgrade_count=3),
        "Brewing Area": ShopUpgradeSpec(upgrade_count=3),
        "Basement": ShopUpgradeSpec(upgrade_count=3),
    }

    def __init__(self):
        super().__init__()

        starting_items: list[StartingItemData] = []

        starting_items.append(
            {"item_categories": ["Shop Ingredients"], "random": 10},
        )

        for ingredient_name, ingredient in self.ingredients.items():
            self.define_item(
                ingredient_name,
                category="Shop Ingredients",
                useful=True,
            )

        relationship_completion_item_name = self.define_item(
            f"Best Friends",
            category="Best Friends",
            progression=True,
            count=len(self.characters),
        )["name"]

        starting_items.append(
            {"item_categories": ["Characters"], "random": 3},
        )

        for character_name in self.characters:
            self.define_item(
                character_name,
                category="Characters",
                progression=True,
            )

            for relationship_rank in range(
                self.starting_relationship_rank, self.max_relationship_rank + 1
            ):
                relationship_rank_location = self.define_location(
                    f"{character_name} - Rank {relationship_rank}",
                    category=f"{character_name}",
                    requires=f"|{character_name}|",
                )

                if relationship_rank == 7:
                    relationship_rank_location["place_item"] = [
                        relationship_completion_item_name
                    ]

        starting_items.append(
            {"item_categories": ["Cards"], "random": 15},
        )

        for card_name, card in self.cards.items():
            self.define_item(
                card_name,
                category="Cards",
                useful=True,
            )

        starting_items.append(
            {"item_categories": ["Adventure Locations"], "random": 3},
        )

        for (
            adventure_location_name,
            adventure_location,
        ) in self.adventure_locations.items():
            self.define_item(
                adventure_location_name,
                category="Adventure Locations",
                useful=True,
            )

        starting_items.append(
            {"item_categories": ["Cauldrons"], "random": 3},
        )

        for cauldron_name, cauldron in self.cauldrons.items():
            if cauldron.upgrade_count == 0:
                self.define_item(
                    cauldron_name,
                    category="Cauldrons",
                    useful=True,
                )
            else:
                self.define_item(
                    f"Progressive {cauldron_name}",
                    category="Cauldrons",
                    useful=True,
                    count=cauldron.upgrade_count,
                )

                for cauldron_upgrade_index in range(cauldron.upgrade_count + 1):
                    self.define_location(
                        cauldron_name + ("+" * cauldron_upgrade_index),
                        category="Cauldrons",
                    )

        starting_items.append(
            {"item_categories": ["Fuel"], "random": 3},
        )

        for fuel_name in self.fuels:
            self.define_item(
                fuel_name,
                category="Fuel",
                useful=True,
            )

        for shop_upgrade_name, shop_upgrade in self.shop_upgrades.items():
            self.define_item(
                f"Progressive {shop_upgrade_name}",
                category="Shop Upgrades",
                useful=True,
                count=shop_upgrade.upgrade_count,
            )

            for shop_upgrade_index in range(shop_upgrade.upgrade_count):
                self.define_location(
                    f"Level {shop_upgrade_index + 2} {shop_upgrade_name}",
                    category="Shop Upgrades",
                )

        checkpoint_count = 5
        potions_per_checkpoint = 3
        checkpoint_completion_item_name = "Checkpoint Completion"

        starting_items.extend(
            {
                "item_categories": [f"Checkpoint {checkpoint_number} Requirements"],
                "random": potions_per_checkpoint,
            }
            for checkpoint_number in range(1, checkpoint_count + 1)
        )

        for potion_name in self.potions:
            for potion_quality in self.potion_qualities:
                self.define_location(
                    f"{potion_quality} {potion_name}",
                    category="Potions",
                )

                for checkpoint_number in range(1, checkpoint_count + 1):
                    self.define_item(
                        f"Checkpoint {checkpoint_number} Requirement - {potion_quality} {potion_name}",
                        category=[f"Checkpoint {checkpoint_number} Requirements"],
                        local=True,
                        filler=True,
                    )

        self.define_item(
            checkpoint_completion_item_name,
            category="Checkpoint Completion",
            count=checkpoint_count * potions_per_checkpoint,
            progression=True,
        )

        for checkpoint_number in range(1, checkpoint_count + 1):
            for checkpoint_potion_number in range(1, potions_per_checkpoint + 1):
                self.define_location(
                    f"Checkpoint {checkpoint_number} - Potion {checkpoint_potion_number}",
                    category="Checkpoints",
                    requires=f"|{checkpoint_completion_item_name}:{(checkpoint_number - 1) * potions_per_checkpoint}|",
                )

            for guild_investment_number in range(1, 3 + 1):
                self.define_location(
                    f"Checkpoint {checkpoint_number} - Guild Investment {guild_investment_number}",
                    category="Guild Investments (Baptiste)",
                )

            for enchantment_number in range(1, 3 + 1):
                self.define_location(
                    f"Checkpoint {checkpoint_number} - Enchantment {enchantment_number}",
                    category="Enchantments (Roxanne)",
                )

            for chest_number in range(1, 3 + 1):
                self.define_location(
                    f"Checkpoint {checkpoint_number} - Chest {chest_number}",
                    category="Chests (Salt & Pepper)",
                )

            for campaign_number in range(1, 3 + 1):
                self.define_location(
                    f"Checkpoint {checkpoint_number} - Campaign  {campaign_number}",
                    category="Campaigns (Luna)",
                )

        self.define_location(
            "Victory",
            category="Victory",
            requires=f"|{checkpoint_completion_item_name}:all| and |{relationship_completion_item_name}:30%|",
            victory=True,
        )

        self.game["starting_items"] = starting_items


spec = PotionomicsWorldSpec()
