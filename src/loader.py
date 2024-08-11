from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from common import CPContentChange, ExpansionType, SMAPIDependency, SMAPIManifest
from configuration import ASSETS, DEPENDENCIES, MANIFEST, PATCHES


@dataclass
class CharacterAsset:
    name: str
    variants: list[str]
    season: bool
    day_event: bool
    location_name: bool


# <character name>_{{Season}}_{{DayEvent}}_{{LocationName}}_<selected option>
def parse_asset_name(filename: str) -> list[str]:
    return filename.removesuffix(".png").split("_")


def get_character_dirs(expansion: ExpansionType = ExpansionType.BASE) -> list[Path]:
    return [character for character in ASSETS.joinpath(expansion.value).glob("*")]


def get_character_variants(dir: Path) -> list[str]:
    return [parse_asset_name(asset.name)[-1] for asset in dir.glob("*") if asset.is_file()]


def get_character_variant_map(expansion: ExpansionType = ExpansionType.BASE) -> dict[str, list[str]]:
    return {dir.name: get_character_variants(dir) for dir in get_character_dirs(expansion)}


def get_character_asset(dir: Path) -> CharacterAsset:
    character = CharacterAsset(
        name=dir.name,
        variants=get_character_variants(dir),
        season=dir.joinpath("Season").exists(),
        day_event=dir.joinpath("DayEvent").exists(),
        location_name=dir.joinpath("LocationName").exists(),
    )

    return character


def get_character_asset_list(expansion: ExpansionType = ExpansionType.BASE) -> list[CharacterAsset]:
    return [get_character_asset(dir) for dir in get_character_dirs(expansion)]


def load_manifest() -> SMAPIManifest:
    return json.loads(MANIFEST.read_text())


def load_dependencies(expansion: ExpansionType = ExpansionType.BASE) -> list[SMAPIDependency]:
    return json.loads(DEPENDENCIES.joinpath(f"{expansion.value}.json").read_text())


def load_patches(expansion: ExpansionType = ExpansionType.BASE) -> list[CPContentChange]:
    patches_dir = PATCHES.joinpath(expansion.value)
    patches: list[CPContentChange] = [patch for character_patches in patches_dir.glob("*") for patch in json.loads(character_patches.read_text())]

    return patches
