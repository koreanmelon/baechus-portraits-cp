from pathlib import Path

from common import ExpansionType

SVE_UNIQUE_ID = "FlashShifter.SVECode"
SVE_MIN_VERSION = "1.14.19"

ASSETS = Path("assets")
OUTPUT = Path("out")


def mod_output_path(name: str, version: str, exp_type: ExpansionType = ExpansionType.BASE) -> Path:
    return OUTPUT.joinpath(f"{name}-{version}-{exp_type.value}")
