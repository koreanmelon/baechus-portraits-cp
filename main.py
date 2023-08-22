import argparse
import json
import logging
import os
from pathlib import Path
from zipfile import ZipFile

logging.basicConfig(format='%(asctime)s %(levelname)-8s: %(message)s',
                    datefmt='[%m/%d/%Y %I:%M:%S %p]')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BUILD = Path("build")
SRC = Path("src")

DATA = Path("data")
ASSETS = Path(DATA, "assets")


# Parse command line arguments to determine which action to take
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--build", help="Build the mod", action="store_true")
args = parser.parse_args()


bachelors_m = ["Alex", "Elliott", "Harvey", "Sam", "Sebastian", "Shane"]
bachelors_f = ["Abigail", "Emily", "Haley", "Leah", "Maru", "Maru_Hospital", "Penny"]
nonmarriage = ["Caroline", "Clint", "Demetrius", "Dwarf", "Evelyn", "George", "Gus", "Jas", "Jodi", "Kent", "Krobus", "Leo",
               "Lewis", "Linus", "Marnie", "Marlon", "Pam", "Pierre", "Robin", "Sandy", "Vincent", "Willy", "Wizard"]
nongiftable = ["Birdie", "Bouncer", "Gil", "Governer", "Grandpa",
               "Gunther", "Henchman", "Marlon", "Morris", "Mr. Qi", "Professor Snail"]

base_characters = bachelors_m + bachelors_f + nonmarriage + nongiftable

sve_characters = ["Alesia", "Andy", "Camilla", "Claire", "Isaac",
                  "Magnus", "Morgan", "Olivia", "Scarlett", "Sophia", "Susan", "Victor"]

characters = [(name, "base") for name in base_characters] + [(name, "sve") for name in sve_characters]

for name, mod in characters:
    Path(ASSETS, mod, name).mkdir(parents=True, exist_ok=True)

if args.build:

    # Create build directory if it doesn't exist
    BUILD.mkdir(parents=True, exist_ok=True)

    # Validate that all characters have a portrait
    logger.info("Checking portraits...")
    missing = {"base": [], "sve": []}
    for name, mod in characters:
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

    # Write content.json
    logger.info("Writing content.json...")
    content_json = {
        "Format": "1.29.0",
        "ConfigSchema": {
            "SVE": {
                "AllowValues": "true, false",
                "Default": "true"
            }
        },
        "Changes": []
    }

    for name, mod in characters:
        content_json["ConfigSchema"][name] = {
            "AllowValues": "Standard",
            "Default": "Standard"
        }

        content_json["Changes"].append(
            {
                "Action": "EditImage",
                "Target": f"Portraits/{name}",
                "FromFile": f"assets/{mod}/{{{{TargetWithoutPath}}}}/{{{{TargetWithoutPath}}}}_{{{name}}}.png",
                "Update": "OnLocationChange",
                "When": {
                    "HasFile:{{FromFile}}": True
                }
            })

    # Write content.json
    with Path(DATA, "content.json").open("w") as content_file:
        json.dump(content_json, content_file, indent=4)

    logger.info("Finished writing content.json...")

    # Read manifest.json
    logger.info("Reading manifest.json...")
    mod_unique_id = ""
    mod_version = ""
    build_num = 0
    with Path(DATA, "manifest.json").open("r") as manifest_file:
        manifest = json.load(manifest_file)
        mod_unique_id = manifest["UniqueID"]
        mod_version = manifest["Version"]

    with Path("BUILD_NUM").open("r+") as build_num_file:
        build_num = int(build_num_file.readline())
        build_num_file.seek(0)
        build_num_file.write(str(build_num + 1))

    logger.info("Finished reading manifest.json...")

    logger.info("Building zip file...")

    # Create zip file
    with ZipFile(Path(BUILD, f"{mod_unique_id}_{mod_version}_{build_num:03}.zip"), 'w') as zip_obj:
        # Iterate over all the files in directory
        logger.debug(f"DATA_DIR: {DATA}")
        for root, dirs, files in os.walk(DATA):
            logger.debug(f"root: {root}, dirs: {dirs}, files: {files}")
            for filename in files:
                infilePath = Path(root, filename)
                outfilePath = Path(mod_unique_id, filename)

                zip_obj.write(infilePath, outfilePath)

        logger.debug(f"ASSETS_DIR: {ASSETS}")
        for root, dirs, files in os.walk(ASSETS):
            logger.debug(f"root: {root}, dirs: {dirs}, files: {files}")
            for filename in files:
                infilePath = Path(root, filename)
                outfilePath = Path(mod_unique_id, root, filename)

                zip_obj.write(infilePath, outfilePath)

    logger.info("Finished building zip file...")

    logger.info("Done!")
