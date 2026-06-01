from argparse import ArgumentParser
from mcaddon import __version__, PackageFormat, VersionBump
from mclang import tl
import logging
import sys
import string

from mcaddon.contrib.logviewer import LogViewer

from .packager import Packager
from .config import PackagerConfig
from mcaddon.contrib.tkpackager import TkPackager

logging.basicConfig(
    format="[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s",
    datefmt="%I:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
    level=logging.INFO,
)

api = Packager(logger=True)

parser = ArgumentParser(prog="mcaddon", description=tl("cli.mcaddon"))
parser.add_argument(
    "-V",
    "--version",
    action="store_true",
    help=tl("cli.mcaddon.version"),
)

# Parser
subparsers = parser.add_subparsers(dest="tool", required=True)

spec1 = subparsers.add_parser("show", help=tl("cli.mcaddon.show"))

spec2 = subparsers.add_parser("logviewer", help=tl("cli.mcaddon.logviewer"))

# package <package> -rp <path> -bp <path>
spec3 = subparsers.add_parser("package", help=tl("cli.mcaddon.package"))
spec3.add_argument(dest="output", type=str, help=tl("cli.mcaddon.package.output"))

# content
spec3.add_argument(
    "-rp",
    "--resource-pack",
    dest="resource_packs",
    type=str,
    action="append",
    default=[],
    help=tl("cli.mcaddon.package.resourcePacks"),
)
spec3.add_argument(
    "-bp",
    "--behavior-pack",
    dest="behavior_packs",
    type=str,
    action="append",
    default=[],
    help=tl("cli.mcaddon.package.behaviorPacks"),
)
spec3.add_argument(
    "-sp",
    "--skin-pack",
    dest="skin_packs",
    type=str,
    action="append",
    default=[],
    help=tl("cli.mcaddon.package.skinPacks"),
)
spec3.add_argument(
    "--marketing-art",
    dest="marketing_art",
    type=str,
    action="append",
    default=[],
    help=tl("cli.mcaddon.package.marketingArt"),
)
spec3.add_argument(
    "--store-art",
    dest="store_art",
    type=str,
    action="append",
    default=[],
    help=tl("cli.mcaddon.package.storeArt"),
)
spec3.add_argument(
    "-w",
    "--world",
    type=str,
    help=tl("cli.mcaddon.package.world"),
)

# flags
spec3.add_argument(
    "--config",
    type=str,
    help=tl("cli.mcaddon.package.config"),
)
spec3.add_argument(
    "--format",
    type=PackageFormat,
    choices=PackageFormat,
    help=tl("cli.mcaddon.package.format"),
)
spec3.add_argument(
    "--bump",
    type=VersionBump,
    choices=VersionBump,
    help=tl("cli.mcaddon.package.bump"),
)

# Tools
for tool in api.tools.keys():
    name = "".join([char for char in tool if char in set(string.ascii_letters)])
    spec3.add_argument(
        f"--{name}",
        action="store_true",
        help=tl(f"cli.mcaddon.package.{name}"),
    )


def main() -> int:
    args = parser.parse_args()
    if args.version:
        print(f"mcaddon {__version__}")
        return 1

    match args.tool:
        case "package":
            config = PackagerConfig.from_namespace(args)
            config.update(PackagerConfig.from_file(args.config))
            api.build(args.output, config)

        case "show":
            app = TkPackager()
            app.mainloop()

        case "logviewer":
            app = LogViewer()
            app.mainloop()
    return 0


if __name__ == "__main__":
    main()
