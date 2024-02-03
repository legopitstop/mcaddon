from argparse import ArgumentParser
from mcaddon import __version__

parser = ArgumentParser()
parser.add_argument(
    "-V",
    "--version",
    action="store_true",
    help="print the mcaddon version number and exit.",
)

# build current project
# Add file to mcpack
# Add mcpack to mcaddon
# Merge mcpack and/or mcaddon


def main():
    args = parser.parse_args()
    if args.version:
        print(__version__)


if __name__ == "__main__":
    main()
