from __future__ import annotations

from common import CPContentSpec, ExpansionType
from loader import get_character_asset_list, get_character_variant_map


def build_config(expansion: ExpansionType = ExpansionType.BASE):
    character_variant_map = get_character_variant_map(expansion)

    config: dict[str, str] = {name: "Standard" for name in character_variant_map.keys()}
    return config


def build_content(expansion: ExpansionType = ExpansionType.BASE) -> CPContentSpec:
    character_variant_map = get_character_variant_map(expansion)

    content: CPContentSpec = {
        "Format": "2.3.0",
        "ConfigSchema": {"SeasonalPortraits": {"AllowValues": "true, false", "Default": True}},
        "Changes": [],
    }

    content["ConfigSchema"] |= {name: {"AllowValues": ", ".join(variants), "Default": "Standard"} for name, variants in character_variant_map.items()}
    content["Changes"].extend(
        {
            "Action": "EditImage",
            "Target": f"Portraits/{name}",
            "FromFile": f"assets/{expansion.value}/{name}/{name}_{{{{{name}}}}}.png",
            "Update": "OnDayStart",
            "When": {"HasFile:{{FromFile}}": True},
        }
        for name in character_variant_map.keys()
    )

    for asset in get_character_asset_list(expansion):
        if asset.season:
            content["Changes"].append(
                {
                    "Action": "EditImage",
                    "Target": f"Portraits/{asset.name}",
                    "FromFile": f"assets/{expansion.value}/{asset.name}/Season/{asset.name}_{{{{Season}}}}_{{{{{asset.name}}}}}.png",
                    "Update": "OnLocationChange",
                    "When": {"HasFile:{{FromFile}}": True, "SeasonalPortraits": True},
                }
            )

        if asset.day_event:
            content["Changes"].append(
                {
                    "Action": "EditImage",
                    "Target": f"Portraits/{asset.name}",
                    "FromFile": f"assets/{expansion.value}/{asset.name}/DayEvent/{asset.name}_{{{{DayEvent}}}}_{{{{{asset.name}}}}}.png",
                    "Update": "OnLocationChange",
                    "When": {"HasFile:{{FromFile}}": True},
                }
            )

        if asset.location_name:
            content["Changes"].append(
                {
                    "Action": "EditImage",
                    "Target": f"Portraits/{asset.name}",
                    "FromFile": f"assets/{expansion.value}/{asset.name}/LocationName/{asset.name}_{{{{LocationName}}}}_{{{{{asset.name}}}}}.png",
                    "Update": "OnLocationChange",
                    "When": {"HasFile:{{FromFile}}": True},
                }
            )

    return content
