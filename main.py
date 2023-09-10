import argparse
import json
import logging
from pathlib import Path

from src.builder import (BUILD, ASSETS, CPBuilder, ModType)

logging.basicConfig(format='%(asctime)s %(levelname)-8s: %(message)s',
                    datefmt='[%m/%d/%Y %I:%M:%S %p]')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Parse command line arguments to determine which action to take
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--build", help="Build the mod", action="store_true")
parser.add_argument("-d", "--dev", help="Build in development mode", action="store_true")
args = parser.parse_args()


bachelors_m = ["Alex", "Elliott", "Harvey", "Sam", "Sebastian", "Shane"]
bachelors_f = ["Abigail", "Emily", "Haley", "Leah", "Maru", "Maru_Hospital", "Penny"]
nonmarriage = ["Caroline", "Clint", "Demetrius", "Dwarf", "Evelyn", "George", "Gus", "Jas", "Jodi", "Kent", "Krobus", "Leo",
               "Lewis", "Linus", "Marnie", "Pam", "Pierre", "Robin", "Sandy", "Vincent", "Willy", "Wizard"]
nongiftable = ["Birdie", "Bouncer", "Gil", "Governer", "Grandpa",
               "Gunther", "Henchman", "Marlon", "Morris", "Mr. Qi", "Professor Snail"]

base_characters = bachelors_m + bachelors_f + nonmarriage + nongiftable

sve_characters = ["Alesia", "Andy", "Camilla", "Claire", "Isaac",
                  "Magnus", "Morgan", "Olivia", "Scarlett", "Sophia", "Susan", "Victor"]


characters = [(name, "base", ["Standard"]) for name in base_characters] + \
    [(name, "sve", ["Standard"]) for name in sve_characters]

mod_json = json.load(Path("mod.json").open("r"))
variants = mod_json["config"]["variants"]
characters = [(name, mod, styles + variants[name] if name in variants else styles) for name, mod, styles in characters]

for name, mod, _ in characters:
    Path(ASSETS, mod, name).mkdir(parents=True, exist_ok=True)

if args.build:
    # Create build directory if it doesn't exist

    # Validate that all characters have a portrait
    logger.info("Checking portraits...")
    missing = {"base": [], "sve": []}
    for name, mod, _ in characters:
        std_portrait = Path(ASSETS, mod, name, f"{name}_Standard.png")
        if not std_portrait.exists():
            portrait = Path(ASSETS, mod, name, f"{name}.png")
            if portrait.exists():
                portrait.rename(std_portrait)
            else:
                missing[mod].append(f"{name}_Standard.png")

    logger.warning(f"Missing some portraits: {len(missing['base'])} base, {len(missing['sve'])} sve")
    for mod, names in missing.items():
        logger.debug(f"{mod} ({len(names)}): {names}")

    # content_json_sve = copy.deepcopy(content_json_base)

    # Build base content pack
    logger.info("Building content pack for base")
    base = CPBuilder(
        mod_json=mod_json,
        mod_type=ModType.BASE,
        characters=characters
    )
    base.build()

    # Build SVE content pack
    logger.info("Building content pack for sve")
    sve = CPBuilder(
        mod_json=mod_json,
        mod_type=ModType.SVE,
        characters=characters
    )
    sve.build()

    logger.info("Done!")
