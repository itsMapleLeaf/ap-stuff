import json
from ..lib.manual_worlds import find_local_manual_world_projects

if __name__ != "__main__":
    raise RuntimeError("This file is only meant to be run as a script.")

for project in find_local_manual_world_projects():
    with open(project.path / "archipelago.json", "w") as manifest_file:
        manifest_data = {
            "game": project.world_id,
            "authors": ["MapleLeaf"],
            "version": 7,
            "compatible_version": 7,
            "world_version": "1.0.0",
            "minimum_ap_version": "0.6.4",
        }
        json.dump(manifest_data, manifest_file, indent=4)
