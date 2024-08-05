import argparse
import json
import logging
import shutil
from pathlib import Path

from builder import build_config, build_content
from common import ExpansionType
from configuration import ASSETS, mod_output_path
from loader import load_manifest


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
    # parser.add_argument(
    #     "-e",
    #     "--expansion",
    #     help="Specifies which expansions to include in the content pack.",
    #     action="store",
    #     default=None,
    # )

    args = parser.parse_args()

    level: str = args.level
    logger.setLevel(logging.getLevelNamesMapping()[level])

    # expansions: list[ExpansionType] = [ExpansionType.BASE]
    # if args.expansion is not None:
    #     expansions.append(ExpansionType[args.expansion.upper()])

    # Load manifest.json
    manifest_json = load_manifest(Path("manifest-base.template.json"))

    # Build content.json
    content_json = build_content()

    # Builder config.json
    config_json = build_config()

    mod_id = manifest_json["UniqueID"]
    mod_version = manifest_json["Version"]

    output_dir = mod_output_path(mod_id, mod_version)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_dir.joinpath("manifest.json").write_text(json.dumps(manifest_json, indent=4))
    output_dir.joinpath("content.json").write_text(json.dumps(content_json, indent=4))
    output_dir.joinpath("config.json").write_text(json.dumps(config_json, indent=4))

    shutil.copytree(
        src=ASSETS.joinpath(ExpansionType.BASE.value),
        dst=output_dir.joinpath("assets", ExpansionType.BASE.value),
        dirs_exist_ok=True,
    )


if __name__ == "__main__":
    main()
