from .world import WorldSpec


arcade_levels = {
    "Ignition": [
        "Chroma",
        "Vector Valley",
        "Static Fire Signal",
        "Shallow",
        "Incline",
        "Station",
        "Whisper",
        "Particular Journey",
        "Turbines",
        "COAT Speedway",
        "Tharsis Tholus",
    ],
    "High Impact": [
        "Virtual Rift",
        "Sea",
        "Beta Echoes",
        "Sender",
        "Absorption",
        "Fiber",
        "Homestead",
        "Salmon",
        "The Manor",
        "Uncanny Valley",
        "Sakura Skyway",
        "Le Teleputo",
        "Method",
        "Binary Construct",
        "Storm 2 - Neon Thunder",
        "Amusement",
        "Outrun",
        "Iris",
    ],
    "Brute Force": [
        "Volcanic Rush",
        "Ruin",
        "Moonlight",
        "Instability",
        "Shafty",
        "Precept",
        "Aeris",
        "Overdrive",
        "Floral",
        "Past",
        "Neo Seoul",
        "Event Horizon",
        "Yellow",
        "Sugar Rush",
        "Sword",
        "Forsaken Shrine",
        "Toy Time",
        "Noir",
        "Brink",
        "Projection",
        "Vibe",
        "Luminescence",
    ],
    "Overdrive": [
        "Paradise Lost",
        "Epicentre",
        "Neo Seoul II",
        "Serenity",
        "Red",
        "Table",
        "Knowledge",
        "Pacebreaker",
        "White",
        "Tetreal",
        "Mentality",
        "Wired",
        "Hardline",
        "Gravity",
        "Digital",
        "Monument",
        "Fulcrum",
        "SR Motorplex",
        "Hard Light Transfer",
        "Impulse",
        "Observatory",
        "Earth",
        "Eclipse",
        "Shrine",
        "Liminal",
        "White Lightning Returns",
    ],
    "Nightmare Fuel": [
        "Affect",
        "The Night Before",
        "Industrial Fury",
        "Fallback Protocol",
        "Cosmic Glitch",
        "Orthodox",
        "Zenith",
        "Micro",
        "Candles of Hekate",
        "Sector 0",
        "Macro",
        "Glide in the Hole",
        "Inferno",
    ],
    "Legacy": [
        "Broken Symmetry",
        "Lost Society",
        "Negative Space",
        "Departure",
        "Ground Zero",
        "The Observer Effect",
        "Aftermath",
        "Friction",
        "The Thing About Machines",
        "Corruption",
        "Dissolution",
        "Falling Through",
        "Monolith",
        "Destination Unknown",
        "Rooftops",
        "Factory",
        "Stronghold",
        "Approach",
        "Continuum",
        "Escape",
    ],
}

campaign_levels = {
    "Adventure": [
        "Instantiation",
        "Cataclysm",
        "Diversion",
        "Euphoria",
        "Entanglement",
        "Automation",
        "Abyss",
        "Embers",
        "Isolation",
        "Repulsion",
        "Compression",
        "Research",
        "Contagion",
        "Overload",
        "Ascension",
        "Enemy",
    ],
    "Lost to Echoes": [
        "Long Ago",
        "Forgotten Utopia",
        "A Deeper Void",
        "Eye of the Storm",
        "The Sentinel Still Watches",
        "Shadow of the Beast",
        "Pulse of a Violent Heart",
        "It Was Supposed To Be Perfect",
        "Echoes",
    ],
    "Nexus": [
        "Mobilization",
        "Resonance",
        "Deterrence",
        "Terminus",
        "Collapse",
    ],
}

spec = WorldSpec(
    starting_items=[
        {"item_categories": ["Arcade"], "random": 7},
    ]
)

# levels are unlocked individually
for arcade_set_name, arcade_level_names in arcade_levels.items():
    for arcade_level_index, arcade_level_name in enumerate(arcade_level_names):
        arcade_level_item = spec.define_item(
            f"Arcade - {arcade_set_name} {arcade_level_index + 1:02d} - {arcade_level_name}",
            category=f"Arcade",
            progression=True,
        )

        spec.define_location(
            arcade_level_item["name"],
            category=f"Arcade - {arcade_set_name}",
            requires=f"|{arcade_level_item['name']}|",
        )

for campaign_name, campaign_level_names in campaign_levels.items():
    # campaigns are unlocked on a per-campaign basis instead of per level
    campaign_item = spec.define_item(
        f"Campaign - {campaign_name}",
        category=f"Campaign",
        progression=True,
    )

    for campaign_level_index, campaign_level_name in enumerate(campaign_level_names):
        spec.define_location(
            f"Campaign - {campaign_name} {campaign_level_index + 1:02d} - {campaign_level_name}",
            category=f"Campaign - {campaign_name}",
            requires=f"|{campaign_item['name']}|",
        )

spec.define_item(
    "Decryption",
    category="Decryption",
    progression=True,
    count=20,
)

spec.define_location(
    "Decryption Success",
    category="Victory",
    requires="|Decryption:70%|",
    victory=True,
)
