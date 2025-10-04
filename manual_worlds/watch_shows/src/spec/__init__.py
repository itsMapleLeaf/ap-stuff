from .requires import Requires
from .world import WorldSpec

spec = WorldSpec()

# TODO: make this options... somehow
shows = {
    "Shinsekai yori": {"episodes": 25, "starting_episode": 0},
    "ZENSHU": {"episodes": 12, "starting_episode": 4},
    "A Sign of Affection": {"episodes": 12, "starting_episode": 0},
    "Keep Your Hands Off Eizouken!": {"episodes": 12, "starting_episode": 0},
    "BanG Dream! It's MyGO!!!!!": {"episodes": 13, "starting_episode": 10},
    "Ameku M.D. Doctor Detective": {"episodes": 12, "starting_episode": 10},
    "Log Horizon 2": {"episodes": 25, "starting_episode": 0},
    "86 EIGHTY-SIX Part 2": {"episodes": 12, "starting_episode": 4},
}

spec.game["starting_items"] = [
    {"item_categories": ["Shows"], "random": len(shows) + 5},
]

spec.define_item(
    "Last Episode",
    category="Victory",
    progression=True,
    count=len(shows),
)

spec.define_location(
    "why is this so hard",
    category="Victory",
    requires=Requires.item("Last Episode", "50%"),
    victory=True,
)

for show, show_info in shows.items():
    spec.define_item(
        f"{show} - Progressive Episodes",
        category="Shows",
        progression=True,
        count=show_info["episodes"] - show_info["starting_episode"],
    )

    for episode_index in range(show_info["episodes"] - show_info["starting_episode"]):
        episode = episode_index + show_info["starting_episode"] + 1

        episode_location = spec.define_location(
            f"{show} - Episode {episode}",
            category=f"Shows - {show}",
            requires=Requires.item(f"{show} - Progressive Episodes", episode_index + 1),
        )

        if episode == show_info["episodes"]:
            episode_location["place_item"] = ["Last Episode"]
