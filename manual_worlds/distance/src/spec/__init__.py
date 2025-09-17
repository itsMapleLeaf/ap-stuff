from .world import WorldSpec

spec = WorldSpec(
    starting_items=[
        {"item_categories": ["Arcade"], "random": 5},
    ]
)

arcade_level_sets = {
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
    "Challenge": [
        "Dodge",
        "44 Second Theory",
        "Transfer",
        "Divide",
        "Thunder Struck",
        "Electric",
        "Descent",
        "Disassembly Line",
        "Red Heat",
        "Grinder",
        "Detached",
        "Elevation",
        "Obsidian",
        "Hexahorrific",
        "Too Many Dots",
        "Variant Blue",
        "Biotec 4",
    ],
}

for arcade_set_name, arcade_level_names in arcade_level_sets.items():
    (arcade_set_option_name, _) = spec.define_toggle_option(
        f"enable_arcade_set_{arcade_set_name.lower().replace(' ', '_')}",
        display_name=f"Enable {arcade_set_name} Levels",
        description=f"Enable levels from the {arcade_set_name} arcade set",
        default=True,
    )

    (arcade_set_category_name, _) = spec.define_category(
        f"Arcade - {arcade_set_name}",
        yaml_option=[arcade_set_option_name],
    )

    # arcade levels are unlocked individually
    for arcade_level_index, arcade_level_name in enumerate(arcade_level_names):
        arcade_level_item = spec.define_item(
            f"{arcade_level_index + 1:02d} {arcade_level_name} ({arcade_set_name})",
            category=[f"Arcade", arcade_set_category_name],
            progression=True,
        )

        spec.define_location(
            arcade_level_item["name"],
            category=arcade_set_category_name,
            requires=f"|{arcade_level_item['name']}|",
        )


campaigns = {
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

for campaign_name, campaign_level_names in campaigns.items():
    (campaign_option_name, _) = spec.define_toggle_option(
        f"enable_campaign_{campaign_name.lower().replace(' ', '_')}",
        display_name=f"Enable {campaign_name} Campaign",
        description=f"Enable the {campaign_name} campaign",
        default=True,
    )

    (campaign_category_name, _) = spec.define_category(
        f"Campaign - {campaign_name}",
        yaml_option=[campaign_option_name],
    )

    # campaigns are unlocked on a per-campaign basis instead of per level
    campaign_item = spec.define_item(
        campaign_category_name,
        category=f"Campaign",
        progression=True,
    )

    for campaign_level_index, campaign_level_name in enumerate(campaign_level_names):
        spec.define_location(
            f"{campaign_level_index + 1:02d} {campaign_level_name} ({campaign_name})",
            category=campaign_category_name,
            requires=f"|{campaign_item['name']}|",
        )


spec.define_item(
    "Decryption",
    category="Decryption",
    progression=True,
    count=10,
)

spec.define_location(
    "Decryption Success",
    category="Victory",
    requires="|Decryption:70%|",
    victory=True,
)
