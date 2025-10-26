from pathlib import Path
from typing import Final


project_dir: Final = Path(__file__).parent.parent
worlds_dir: Final = project_dir / "manual_worlds"

# user_archipelago_dir: Final = Path("C:/ProgramData/Archipelago")
user_archipelago_dir: Final = project_dir / "archipelago"
user_archipelago_worlds_dir: Final = user_archipelago_dir / "custom_worlds"
user_archipelago_players_dir: Final = user_archipelago_dir / "Players"
user_archipelago_templates_dir: Final = user_archipelago_dir / "Players/Templates"

dist_dir: Final = project_dir / "dist"
dist_generate_dir: Final = dist_dir / "generate"
dist_generate_players_dir: Final = dist_generate_dir / "players"
