import argparse
import json
import logging
import shutil
from typing import Optional

from builder import build_config, build_content
from common import ExpansionType
from configuration import ASSETS, OUTPUT, mod_output_path
from loader import load_dependencies, load_manifest


def main():
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s: %(message)s",
        datefmt="[%m/%d/%Y %I:%M:%S %p]",
    )
    logger = logging.getLogger()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--level",
        help="Sets the logging level",
        action="store",
        choices=logging.getLevelNamesMapping().keys(),
        default="NOTSET",
    )
    parser.add_argument(
        "-e",
        "--expansions",
        help="Specifies which expansions to include in the content pack.",
        action="append",
        choices=[ExpansionType.SVE.name],
        default=None,
    )

    args = parser.parse_args()

    level: str = args.level
    logger.setLevel(logging.getLevelNamesMapping()[level])

    include_expansions: Optional[list[str]] = args.expansions

    expansions: list[ExpansionType] = [ExpansionType.BASE]
    if include_expansions is not None:
        expansions.extend([ExpansionType[expansion] for expansion in include_expansions])

    # Load manifest.json
    manifest_json = load_manifest()

    # Build content.json
    content_json = build_content()

    # Builder config.json
    config_json = build_config()

    # Handle expansions
    for expansion in expansions:
        if expansion == ExpansionType.BASE:
            continue

        dependencies = load_dependencies(expansion)
        manifest_json["Dependencies"].extend(dependencies)

        expansion_content = build_content(expansion)
        content_json["ConfigSchema"] |= expansion_content["ConfigSchema"]
        content_json["Changes"].extend(expansion_content["Changes"])

        expansion_config = build_config(expansion)
        config_json |= expansion_config

    # Create outputs
    mod_id = manifest_json["UniqueID"]
    mod_version = manifest_json["Version"]

    output_dir = mod_output_path(mod_id, mod_version, expansions)
    output_dir.mkdir(parents=True, exist_ok=True)

    for expansion in expansions:
        shutil.copytree(
            src=ASSETS.joinpath(expansion.value),
            dst=output_dir.joinpath("assets", expansion.value),
            dirs_exist_ok=True,
        )

    output_dir.joinpath("manifest.json").write_text(json.dumps(manifest_json, indent=4))
    output_dir.joinpath("content.json").write_text(json.dumps(content_json, indent=4))
    output_dir.joinpath("config.json").write_text(json.dumps(config_json, indent=4))

    # Consumed by GitHub Actions
    OUTPUT.joinpath("LATEST").write_text(mod_version)


if __name__ == "__main__":
    main()
