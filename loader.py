from __future__ import annotations

from pathlib import Path

from common import ExpansionType
from configuration import ASSETS


def get_character_dirs(expansion: ExpansionType = ExpansionType.BASE) -> list[Path]:
    return [character for character in ASSETS.joinpath(expansion.value).glob("*")]


def get_character_variants(dir: Path) -> list[str]:
    return [asset.name.removeprefix(f"{dir.name}_").removesuffix(".png") for asset in dir.glob("*")]


def get_character_variant_map(expansion: ExpansionType = ExpansionType.BASE) -> dict[str, list[str]]:
    return {dir.name: get_character_variants(dir) for dir in get_character_dirs(expansion)}
