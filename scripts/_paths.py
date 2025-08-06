from pathlib import Path


project_dir = Path(__file__).parent.parent
worlds_dir = project_dir / "manual_worlds"

# TODO: figure out based on system and/or make configurable
user_archipelago_dir = Path("C:/ProgramData/Archipelago")
user_archipelago_worlds_dir = user_archipelago_dir / "custom_worlds"
