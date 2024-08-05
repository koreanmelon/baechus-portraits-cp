from __future__ import annotations

import json
from pathlib import Path

from common import CPContentSpec, ExpansionType, SMAPIManifest
from configuration import SVE_MIN_VERSION, SVE_UNIQUE_ID
from loader import get_character_variant_map


def build_config(expansion: ExpansionType = ExpansionType.BASE):
    character_variant_map = get_character_variant_map(expansion)

    config: dict[str, str] = {name: "Standard" for name in character_variant_map.keys()}
    return config


def build_content(expansion: ExpansionType = ExpansionType.BASE):
    character_variant_map = get_character_variant_map(expansion)

    content: CPContentSpec = {
        "Format": "2.3.0",
        "ConfigSchema": {
            name: {"AllowValues": ", ".join(variants), "Default": "Standard"}
            for name, variants in character_variant_map.items()
        },
        "Changes": [
            {
                "Action": "Load",
                "Target": f"Portraits/{name}",
                "FromFile": f"assets/base/{{{{TargetWithoutPath}}}}/{{{{TargetWithoutPath}}}}_{{{{{name}}}}}.png",
                "Update": "OnLocationChange",
                "When": {"HasFile:{{FromFile}}": True},
            }
            for name in character_variant_map.keys()
        ],
    }

    return content


def build_manifest(template_file: Path, exp_type: ExpansionType = ExpansionType.BASE):
    manifest: SMAPIManifest = json.loads(template_file.read_text())

    if exp_type == ExpansionType.SVE:
        manifest["Dependencies"].append({"UniqueID": SVE_UNIQUE_ID, "MinimumVersion": SVE_MIN_VERSION})

    return manifest
