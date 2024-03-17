from argparse import ArgumentParser
from mcaddon import __version__, BehaviorPack, Pack
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
import warnings
import os
import time
import traceback

parser = ArgumentParser()
parser.add_argument(
    "-V",
    "--version",
    action="store_true",
    help="print the mcaddon version number and exit.",
)

parser.add_argument(
    "-W",
    "--watch",
    metavar="<file>",
    nargs="?",
    help="Watches this Python file for changes.",
)


# outputs = parser.add_mutually_exclusive_group()
# outputs.add_argument(
#     "-m", "--merge", metavar="<file>", help="merge mcaddon or mcpack into a file"
# )
# parser.add_argument("file", metavar="<file>", help="the target file")

# build current project
# Add file to mcpack
# Add mcpack to mcaddon
# Merge mcpack and/or mcaddon
# Open UI creator in current dir
# Watch python file for changes to build automatically

# mcaddon <file> -m <file>


def main():
    args = parser.parse_args()
    if args.version:
        print(__version__)

    # root = BehaviorPack.load(args.file)
    # try:
    #     if args.merge:
    #         merge(root, args.merge)
    # except Exception as exc:
    #     parser.error(f"{exc}")

    # Should be at end
    if args.watch:
        watch(args.watch)


def merge(file: Pack, merge: str):
    print(file)
    with BehaviorPack.open(merge) as fd2:
        print(fd2)


class FileObserver(FileSystemEventHandler):
    def on_modified(self, event: FileSystemEvent) -> None:
        if (
            not event.is_directory
            and event.event_type == "modified"
            and event.src_path.endswith(".py")
        ):
            print("Executing...")
            with open(event.src_path) as fd:
                try:
                    eval(compile(fd.read(), "<string>", "exec"))
                except Exception as err:
                    traceback.print_exception(err)
        return super().on_modified(event)


def watch(file: str):
    # Interface should be similar to flask
    warnings.warn("This feature is experimental and requires more testing!")
    fp = os.path.abspath(file)
    observer = Observer()
    observer.schedule(FileObserver(), path=fp, recursive=False)
    observer.start()
    print(f"Watching {repr(fp)}. Press Ctrl-c to stop")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    print("Stopping...")
    observer.join()


if __name__ == "__main__":
    main()
