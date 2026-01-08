from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from ..lib.paths import project_dir


with TemporaryDirectory() as temp_dir:
    shutil.copytree(
        project_dir / "ap_bridge",
        Path(temp_dir) / "ap_bridge",
        ignore=shutil.ignore_patterns(
            "__pycache__",
            "__pycache__/*",
            "*/__pycache__",
            "*/__pycache__/*",
        ),
    )

    zip = Path(shutil.make_archive("ap_bridge", format="zip", root_dir=temp_dir))
    dest = project_dir / "downloads" / zip.with_suffix(".apworld").name
    dest.unlink(missing_ok=True)
    zip.rename(dest)
