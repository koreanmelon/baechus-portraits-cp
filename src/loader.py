import json
import logging
from pathlib import Path

from src.builder import ModType

logger = logging.getLogger("__main__")


class Loader:
    def __init__(self) -> None:
        self.characters = None
        self.mod_json = None

        self.assets_dir = Path("assets")

    def load_assets(self):
        logger.info("Loading assets...")

        # Load mod.json
        logger.debug("Loading mod.json...")

        self.mod_json = json.load(Path("mod.json").open("r"))

        bachelors_m = self.mod_json["config"]["characters"]["bachelors_m"]
        bachelors_f = self.mod_json["config"]["characters"]["bachelors_f"]
        nonmarriage = self.mod_json["config"]["characters"]["nonmarriage"]
        nongiftable = self.mod_json["config"]["characters"]["nongiftable"]

        base_character_names = bachelors_m + bachelors_f + nonmarriage + nongiftable
        sve_character_names = self.mod_json["config"]["characters"][ModType.SVE.value]

        variants = self.mod_json["config"]["variants"]

        # Load character names and metadata to memory
        logger.debug("Loading character names and metadata to memory")

        self.characters = []
        for name in base_character_names:
            styles = ["Standard"]
            if name in variants:
                styles.extend(variants[name])

            self.characters.append((name, ModType.BASE.value, styles))

        for name in sve_character_names:
            styles = ["Standard"]
            if name in variants:
                styles.extend(variants[name])

            self.characters.append((name, ModType.SVE.value, styles))

        # Create asset directories for all characters
        logger.debug("Creating asset directories for characters...")

        for name, mod, _ in self.characters:
            Path(self.assets_dir, mod, name).mkdir(parents=True, exist_ok=True)

        # Validate that all characters have a portrait
        logger.debug("Validating existence of all character portraits...")

        missing = {ModType.BASE.value: [], ModType.SVE.value: []}
        for name, mod, _ in self.characters:
            std_portrait = Path(self.assets_dir, mod, name, f"{name}_Standard.png")
            if not std_portrait.exists():
                portrait = Path(self.assets_dir, mod, name, f"{name}.png")
                if portrait.exists():
                    portrait.rename(std_portrait)
                else:
                    missing[mod].append(f"{name}_Standard.png")

        logger.warning(
            f"Missing some portraits: {len(missing[ModType.BASE.value])} {ModType.BASE.value}, {len(missing[ModType.SVE.value])} {ModType.SVE.value}")

        for mod, names in missing.items():
            logger.debug(f"{mod} ({len(names)}): {names}")

        return self.mod_json, self.characters
