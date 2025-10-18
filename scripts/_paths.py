from pathlib import Path


project_dir = Path(__file__).parent.parent
worlds_dir = project_dir / "manual_worlds"

# user_archipelago_dir = Path("C:/ProgramData/Archipelago")
user_archipelago_dir = project_dir / "archipelago"
user_archipelago_worlds_dir = user_archipelago_dir / "custom_worlds"
user_archipelago_templates_dir = user_archipelago_dir / "Players/Templates"
