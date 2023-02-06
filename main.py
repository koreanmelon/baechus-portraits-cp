import argparse
import json
import os
from zipfile import ZipFile

# Parse command line arguments to determine which action to take
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--build", help="Build the mod", action="store_true")
args = parser.parse_args()

if args.build:
    # Create build directory if it doesn't exist
    if not os.path.exists("build"):
        os.makedirs("build")

    # Read the manifest.json
    mod_unique_id = ""
    mod_version = ""
    build_num = 0
    with open("src/manifest.json", "r") as manifest_file:
        manifest = json.load(manifest_file)
        mod_unique_id = manifest["UniqueID"]
        mod_version = manifest["Version"]
    
    with open("./BUILD_NUM", "r+") as build_num_file:
        build_num = int(build_num_file.readline())
        build_num_file.seek(0)
        build_num_file.write(str(build_num + 1))

    # Create zip file
    with ZipFile(os.path.join("build", f"baechus-portraits-cp-v{mod_version}-{build_num}.zip"), 'w') as zip_obj:
        # Iterate over all the files in directory
        for root, dirs, files in os.walk("src"):
            for filename in files:
                infilePath = os.path.join(root, filename)
                outfilePath = os.path.join(mod_unique_id, filename)

                zip_obj.write(infilePath, outfilePath)

        for root, dirs, files in os.walk("assets"):
            for filename in files:
                infilePath = os.path.join(root, filename)
                outfilePath = os.path.join(mod_unique_id, root, filename)

                zip_obj.write(infilePath, outfilePath)
