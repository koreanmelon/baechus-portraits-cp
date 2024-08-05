from __future__ import annotations

import json
from pathlib import Path

from common import ExpansionType, SMAPIManifest
from configuration import ASSETS


def get_character_dirs(expansion: ExpansionType = ExpansionType.BASE) -> list[Path]:
    return [character for character in ASSETS.joinpath(expansion.value).glob("*")]


def get_character_variants(dir: Path) -> list[str]:
    return [asset.name.removeprefix(f"{dir.name}_").removesuffix(".png") for asset in dir.glob("*")]


def get_character_variant_map(expansion: ExpansionType = ExpansionType.BASE) -> dict[str, list[str]]:
    return {dir.name: get_character_variants(dir) for dir in get_character_dirs(expansion)}


def load_manifest(template_file: Path, expansion: ExpansionType = ExpansionType.BASE) -> SMAPIManifest:
    return json.loads(template_file.read_text())
