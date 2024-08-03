import json
import logging
from datetime import datetime
from enum import Enum
from pathlib import Path
from zipfile import ZipFile

logger = logging.getLogger("__main__")


class ModType(Enum):
    BASE = "base"
    SVE = "sve"


class CPBuilder:
    def __init__(self, mod_json: dict, mod_type: ModType, characters: list) -> None:
        assert "Pathoschild.ContentPatcher" in mod_json["dependencies"]

        self.mod_json = mod_json
        self.mod_type = mod_type
        self.characters = characters
        self.manifest_json = None
        self.content_json = None

        self.assets_dir = Path("assets")

        self.build_dir = Path("build")
        self.build_dir.mkdir(parents=True, exist_ok=True)

        self.tmp_dir = Path(self.build_dir, self.mod_type.value)
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

    def build(self):
        logger.info(f"Building content pack ({self.mod_type.value})...")

        self.manifest()
        self.content()
        self.config()

        assert self.manifest_json is not None
        assert self.content_json is not None
        assert self.config_json is not None

        discriminator = datetime.now().strftime("%Y.%m.%d.%H.%M.%S")

        # Write manifest.json
        with Path(self.tmp_dir, "manifest.json").open("w") as manifest_file:
            json.dump(self.manifest_json, manifest_file, indent=4)

        # Write content.json
        with Path(self.tmp_dir, "content.json").open("w") as content_file:
            json.dump(self.content_json, content_file, indent=4)

        # Write config.json
        with Path(self.tmp_dir, "config.json").open("w") as config_file:
            json.dump(self.config_json, config_file, indent=4)

        # Build ZIP file
        logger.debug("Zipping assets and output files...")

        with ZipFile(
            Path(
                self.build_dir,
                f"{self.mod_json['unique_id']}_{self.mod_json['version']}_{discriminator}_{self.mod_type.value}.zip",
            ),
            "w",
        ) as zip:
            # Iterate over all files in directory
            for path in self.assets_dir.glob("**/*"):
                if (ModType.BASE.value in path.parts) or (self.mod_type.value in path.parts):
                    zip.write(path, path.relative_to(self.assets_dir.parent))
                    continue

            for file in self.tmp_dir.glob("*"):
                zip.write(file, file.relative_to(self.tmp_dir))

    def manifest(self):
        logger.debug("Building manifest.json...")

        self.manifest_json = {
            "Name": self.mod_json["name"],
            "Author": self.mod_json["author"],
            "Version": self.mod_json["version"],
            "Description": self.mod_json["description"],
            "UniqueID": self.mod_json["unique_id"],
            "UpdateKeys": self.mod_json["update_keys"],
            "ContentPackFor": {},
            "Dependencies": [],
        }

        if "Pathoschild.ContentPatcher" in self.mod_json["dependencies"].keys():
            self.manifest_json["ContentPackFor"]["UniqueID"] = "Pathoschild.ContentPatcher"

        for dep in self.mod_json["dependencies"].keys():
            if dep == "Pathoschild.ContentPatcher":
                continue

            if self.mod_type == ModType.BASE:
                if dep == "FlashShifter.SVECode":
                    continue

            self.manifest_json["Dependencies"].append(
                {
                    "UniqueID": dep,
                    "MinimumVersion": self.mod_json["dependencies"][dep],
                }
            )

    def content(self):
        logger.debug("Building content.json")

        self.content_json = {
            "Format": self.mod_json["dependencies"]["Pathoschild.ContentPatcher"],
            "ConfigSchema": {},
            "Changes": [],
        }

        for name, mod, styles in self.characters:
            if mod != ModType.BASE.value and mod != self.mod_type.value:
                continue

            self.content_json["ConfigSchema"][name] = {
                "AllowValues": ", ".join(styles),
                "Default": styles[0],
            }

            self.content_json["Changes"].append(
                {
                    "Action": "Load",
                    "Target": f"Portraits/{name}",
                    "FromFile": f"assets/{mod}/{{{{TargetWithoutPath}}}}/{{{{TargetWithoutPath}}}}_{{{{{name}}}}}.png",
                    "Update": "OnLocationChange",
                    "When": {"HasFile:{{FromFile}}": True},
                }
            )

    def config(self):
        logger.debug("Building config.json...")

        self.config_json = {}

        for name, mod, styles in self.characters:
            if mod != ModType.BASE.value and mod != self.mod_type.value:
                continue

            self.config_json[name] = styles[0]
