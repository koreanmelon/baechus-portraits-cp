from enum import Enum
from typing import TypedDict


class SMAPIManifest(TypedDict):
    Name: str
    Author: str
    Version: str
    Description: str
    UniqueID: str
    UpdateKeys: list[str]
    ContentPackFor: dict[str, str]
    Dependencies: list[dict[str, str]]


class CPContentConfigSchemaEntry(TypedDict):
    AllowValues: str
    Default: str


class CPContentChange(TypedDict):
    Action: str
    Target: str
    FromFile: str
    Update: str
    When: dict


class CPContentSpec(TypedDict):
    Format: str
    ConfigSchema: dict[str, CPContentConfigSchemaEntry]
    Changes: list[CPContentChange]


class ExpansionType(Enum):
    BASE = "base"
    SVE = "sve"
