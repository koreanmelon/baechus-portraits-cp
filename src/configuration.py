import os
from pathlib import Path

from common import ExpansionType

ASSETS = Path("assets")
OUTPUT = Path("out")
MANIFEST = Path("manifest.json")
DEPENDENCIES = Path("dependencies")


def mod_output_path(name: str, version: str, expansions: list[ExpansionType] = [ExpansionType.BASE]) -> Path:
    if os.getenv("MOD_BUILD_STAGE") == "prod":
        discriminator = ""
    else:
        import subprocess

        process = subprocess.Popen(["git", "rev-parse", "--short", "HEAD"], shell=False, stdout=subprocess.PIPE)
        discriminator = f"+{process.communicate()[0].strip().decode()}"

    return OUTPUT.joinpath(f"{name}-{version}-{"-".join(expansion.value for expansion in expansions)}{discriminator}")
