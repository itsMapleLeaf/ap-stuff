import re
from .requires import Requires
from .world import WorldSpec


def __define_world_spec() -> WorldSpec:
    spec = WorldSpec()

    songs = {
        "Base Songs": [
            "After Rain - HyuN & MIIM",
            "Reverie - Soba",
            "A Time for Everything - Iris",
            "The Formula - Junk",
            "LostPuppet - rmk",
            "Infinity Heaven - HyuN",
            "심장병 - HyuN feat. HUBOG",
            "別れの序曲 - HyuN feat. Sennzai",
            "Pure White: Tale of Serissa - Sosop",
            "Last Paradise - HyuN feat. Serentium",
            "Beautiful Days - HyuN feat. Ryeorae",
            "Let you DIVE! - HARDCORE TANO*C & エリザベス (CV:大西沙織)",
            "A Clock - kurobe studio",
            "Is This REAL? - SOTUI & NIKITA",
            "終焉から命を救う - MIssionary",
            "無彩色のディストピア - HyuN feat. ウォルピスカーター",
            "Converge - SOTUI x Hundotte",
            "Ice Festival - Nota",
            "BATTLE NO.1 - TANO*C Sound Team",
            "Aurora - Kirara Magic feat. Shion",
            "Snow Magic - Nota",
            "K.Moe (VIP) - ZxNX",
            "Bouquet colore - Nego_tiator",
            "Witches' Party - Kirara Magic feat. Shiroroll",
            "Chrysanthemum - 7mai",
            "Anthem - Silaver & SOTUI",
            "Blastrick - K4Y5",
            "ストレイソウル・アラウンド - みーに",
            "In a Diabolic Manner - Nagiha",
            "Rush E - Sheet Music Boss",
            "Provison - connexio",
            "Make Up Your World feat. キョンシーのCiちゃん & らっぷびと - t+pazolite & Srav3R",
            "Apocalypse - Alice Schach and the Magic Orchestra",
            "Lullaby For an Android - Sad Keyboard Artist feat. AKA",
            "Cynthia - nm-y & 7mai",
            "Awaken In Ruins - Supa7onyz",
            "Shattered Sky After Rain - Lorph & Elexia",
            "Cosmogyral - Altermis & Darren",
            "白菊 -shiragiku- - 立秋",
            "CONVALLARiA - GARNiDELiA",
            "Sword of Convallaria - 崎元仁",
            "Sakura rain - Nanatsukaze",
            "Mirror - peak divide & Rachel Lake",
        ],
        "Chapter 1 - A Journey Begins": [
            "Aqua Theme - HyuN & MIIM",
            "huggy wuggy - ZxNX",
            "Re-waked from Abyss - HeavenEGHD",
            "The Promised Land - Iris feat. LynH",
            "Aqua Stars - Sound Souler",
            # "Inverted World - ARForest",
        ],
        "Chapter 2 - Disaster and Hope": [
            "Secret Illumination - Yooh",
            "Manifold Hypothesis - cybermiso feat. tigerlily",
            "Aorist Hallucination - FallN Leav",
            "Alive - eicateve",
            "Our Message - What's Your Price",
            # "GALACTIC WARZONE - Akira Complex",
        ],
        "Chapter 3 - A Land Divided": [
            "Alfheim's faith - 影虎。",
            "Arbitration - Jun Kuroda",
            "Heaven's Cage - ETIA.",
            "咲く星々 - ユアミトス",
            "シークレット・プラネット - みーに feat. みちとせ",
            "epitaxy - Camellia",
            "Triad of Dryad - MYUKKE.",
            # "翠杜 - 隣の庭は青い(庭師+Aoi)",
        ],
        "Where Our Story Began": [
            "星降る夜と一輪の花 - seatrus",
            "Eternal calm - 長沼浩太(パパ頑張りました)",
            "MAGENTA POTION - EmoCosine",
            "Sense - BilliumMoto × Silentroom",
            "Looking for Stella - Junk",
            "Fate of Aria - HyuN feat.花たん",
        ],
        "HARDCORE TANO*C Collab I": [
            "You & DIE - USAO",
            "Shooting☆Stars - DJ Genki",
            "HiGHER - REDALiCE",
            "Maholova - aran",
            "Recollection - Kobaryo",
            "Lunàtixxx Gear - Laur vs HyuN",
        ],
    }

    (songs_category, _) = spec.define_category(
        "Songs",
        hidden=True,
        starting_count=3,
    )

    for group, group_songs in songs.items():
        for song in group_songs:
            song_item = spec.define_item(
                re.sub(r"\s*[:|]\s*", " ", song),
                category=[songs_category],
                progression=True,
            )
            for difficulty in ["III", "IV"]:
                spec.define_location(
                    f"{song_item["name"]} ({difficulty})",
                    category=[f"Songs - {group}"],
                    requires=Requires.item(song_item),
                )

    challenges = {
        "Chapter 1 - Aquaria": [
            "Bolt's Challenge - Barrel Rolls",
            "Bolt's Challenge - Drifting",
            "Bolt's Challenge - Flicking",
            "Bolt's Challenge - Catching",
            "Stunt Challenge - Suona Champ ft. Rysn",
        ],
        "Chapter 2 - Orb": [
            "Stunt Challenge - Avoid Falling Rocks",
            "Stunt Challenge - First Mining",
            "Stunt Challenge - First Hunting",
            "Bolt's Challenge - Bolt and Lad I",
        ],
        "Chapter 3 - Sylvano": [
            "Bolt's Challenge - Double Stunt Challenge",
            "Stunt Challenge - Ilot Express",
            "Stunt Challenge - Great Escape",
            "Stunt Challenge - Lost Tommy",
            "Stunt Challenge - Great Escape EX",
        ],
        "Where Our Story Began": [
            "Stunt Challenge - Strange Dance",
        ],
    }

    for group, group_challenges in challenges.items():
        for challenge in group_challenges:
            challenge_item = spec.define_item(
                re.sub(r"\s*[:|]\s*", " ", challenge),
                category=["Challenges"],
                progression=True,
            )
            spec.define_location(
                f"{challenge_item['name']}",
                category=[f"Challenges - {group}"],
                requires=Requires.item(challenge_item),
            )

    travel_miles = spec.define_item(
        "Travel Miles",
        category=["Travel Miles"],
        progression=True,
        count=50,
    )

    (boss_completion, _) = spec.define_category(
        "Boss Completion",
        hidden=True,
    )

    boss_completion_1 = spec.define_item(
        "A Journey Begins",
        category=[boss_completion],
        progression=True,
    )["name"]

    spec.define_location(
        "Boss: Inverted World - ARForest",
        category=["Boss Songs"],
        requires=Requires.item(travel_miles, "20%"),
        place_item=[boss_completion_1],
    )

    boss_completion_2 = spec.define_item(
        "Disaster and Hope",
        category=[boss_completion],
        progression=True,
    )["name"]

    spec.define_location(
        "Boss: GALACTIC WARZONE - Akira Complex",
        category=["Boss Songs"],
        requires=Requires.item(travel_miles, "40%"),
        place_item=[boss_completion_2],
    )

    boss_completion_3 = spec.define_item(
        "A Land Divided",
        category=[boss_completion],
        progression=True,
    )["name"]

    spec.define_location(
        "Boss: 翠杜 - 隣の庭は青い(庭師+Aoi)",
        category=["Boss Songs"],
        requires=Requires.item(travel_miles, "60%"),
        place_item=[boss_completion_3],
    )

    spec.define_location(
        "To Be Continued...",
        category=["End"],
        requires=Requires.category(boss_completion, "all"),
        victory=True,
    )

    return spec


spec = __define_world_spec()
