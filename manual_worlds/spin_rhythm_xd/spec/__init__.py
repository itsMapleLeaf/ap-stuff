from ..lib.requires import Requires
from ..lib.world import WorldSpec

songs = [
    # Core Soundtrack
    "2 Mello - cold rock it",
    "2 Mello - Twist Sound",
    "Akira Complex - Dying Scarlet",
    "Akira Complex & PSYQUI - Come to Me",
    "Anamanaguchi - Air on Line",
    "Anomalie - Métropole",
    "Anomalie - Velours",
    "Au5 & Chime - Voidwalkers",
    "Camellia - Body F10ating in the Zero Gravity Space",
    "Camellia - Dance with Silence",
    "Daverwob - Spin Cycle",
    "Douglas Holmquist - Superimposed_RGB",
    "Douglas Holmquist & Susanna Lundgren - Hypersphere",
    "Droptek - Inject",
    "Droptek - Mimic",
    "Eli Way - Daydream",
    "F.O.O.L. - Revenger",
    "F.O.O.L. - Showdown",
    "FarfetchD - Heading East",
    "FarfetchD & Elysium - Coming Too",
    "FLIGHTS - Show Me Love",
    "Haywyre - Let Me Hear That",
    "Haywyre - Never Count on Me",
    "Hyper Potions - New Year",
    "Hyper Potions & Subtact - Adventures",
    "Kitty - I See Lite",
    "Kitty, Rytmeklubben & Lazerdisk - 2 Minutes",
    "Koven - Your Pain",
    "L'Indécis - Second Wind",
    "Lena Raine - Beyond the Heart (Broken Hearts Mix)",
    "Max Brhom - Humanity",
    "Maxo - My Museum",
    "Maxo - Reach You",
    "meganeko - Lights Camera Action",
    "Modern Revolt - VOLT",
    "modus - Engine Start",
    "modus - Sector Five",
    "modus & Loudar - No Limits",
    "Moe Shop & maisou - Lovesick",
    "monomer - Arcana Engine",
    "Nitro Fun - Final Boss",
    "Nitro Fun - New Game",
    "Nitro Fun & Hyper Potions - Checkpoint",
    "Oneeva - Platform 9",
    "Opiuo - Ginger Lizard",
    "Oxford Parker - Robo Trio",
    "Panda Eyes - Colorblind",
    "Panda Eyes & Terminite - Highscore",
    "Pegboard Nerd & Tristam - Razor Sharp",
    "Phonetic Hero - Go Outside",
    "Rogue - Rattlesnake",
    "Rogue - This Is It",
    "seejay - The Magician",
    "Sharks & Chime - Water Elemental",
    "Sharks & Skybreak - Whirlpool",
    "Supathick & Keely Britain - Time",
    "Teminite - Believe",
    "Terminite - Ghost Ship",
    "Terminite - Pirate Afterparty",
    "Terminite - Raise the Black Flag",
    "Terminite - The Kraken",
    "Tokyo Machine - BUBBLES",
    "Tristam & Braken - Flight",
    "Tut Tut Child - Hot Pursuit",
    # Supporter DLC
    "Daverwob - Day Dream",
    # Monstercat DLC
    "Bossfight - U Got Me",
    "FLWR - How We Win",
    "Gammer - THE DROP",
    "Koven - Shut My Mouth",
    "Nitro Fun - Cheat Codes",
    "Notaker & Karra - Into the Light",
    "RIOT - Overkill",
    "Shockone - It's All Over",
    "Tokyo Machine - CRAZY",
    "Xilent - Blue Shadows",
    # Chillhop DLC
    "Brock Berrigan, saib. - Drifter",
    "Eli Way - Green Tea",
    "Ian Ewing - 17",
    "L'Indecis - Playtime",
    "L'Indecis, Moods - Looking for the Sun",
    "Misha, cocabona - Khaleesi",
    "Pandrezz - Takin' You For a Ride",
    "Ruck P - Early Morning",
    "The Kount - Yo",
    "Yasper - Good Friends",
]


class TemplateWorldSpec(WorldSpec):
    def __init__(self):
        super().__init__()

        cd_item = self.define_item(
            "CD",
            category="CDs",
            progression=True,
            count=40,
            local=True,
        )

        self.define_location(
            "Master Spinner XD",
            category="CDs",
            requires=Requires.item(cd_item, "half"),
            victory=True,
        )

        self.define_item(
            "Song Skip",
            category="Song Skips",
            useful=True,
            count=10,
        )

        songs_category = self.define_category(
            "Songs",
            starting_count=5,
        )[0]

        for song in songs:
            song_item = self.define_item(
                song,
                category=[songs_category],
                progression=True,
            )

            for i in range(2):
                self.define_location(
                    f"{song} - {i+1}",
                    category=[f"Songs - {song}"],
                    requires=Requires.item(song_item),
                )


world_spec = TemplateWorldSpec()
