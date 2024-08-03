import argparse
import logging

from builder import CPBuilder, ModType
from loader import Loader

if __name__ == "__main__":
    # Parse command line arguments to determine which action to take
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--level",
        help="Sets the logging level",
        action="store",
        default="notset",
    )

    args = parser.parse_args()

    logging_level_map = {
        "notset": logging.NOTSET,
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s: %(message)s",
        datefmt="[%m/%d/%Y %I:%M:%S %p]",
    )

    logger = logging.getLogger()
    logger.setLevel(logging_level_map[args.level])

    # Load assets
    loader = Loader()
    mod_json, characters = loader.load_assets()

    # Build base content pack
    base = CPBuilder(mod_json=mod_json, mod_type=ModType.BASE, characters=characters)
    base.build()

    # Build SVE content pack
    sve = CPBuilder(mod_json=mod_json, mod_type=ModType.SVE, characters=characters)
    sve.build()
