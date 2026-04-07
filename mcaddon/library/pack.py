__all__ = [
    "resourcepack",
    "behaviorpack",
    "basepack",
    "BasePack",
    "ResourcePack",
    "BehaviorPack",
    "SkinPack",
    "ResourceOutline",
]

from typing import Optional, List, Dict, Generator, Any, Type
from abc import ABC
from uuid import UUID
from PIL import Image
from pathlib import Path
import os
import zipfile
import commentjson
import glob

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from mcaddon.library.world import LevelFile
from mcaddon.core.utils import get_folder_size
from mcaddon.core.file import File, ResourceFile
from .manifest import Manifest


def basepack(start_path: str):
    def wrapper(cls):
        BasePack.add_loader(cls, start_path)
        return cls

    return wrapper


def resourcepack(start_path: str):
    def wrapper(cls):
        ResourcePack.add_loader(cls, start_path)
        return cls

    return wrapper


def behaviorpack(start_path: str):
    def wrapper(cls):
        BehaviorPack.add_loader(cls, start_path)
        return cls

    return wrapper


def skinpack(start_path: str):
    def wrapper(cls):
        SkinPack.add_loader(cls, start_path)
        return cls

    return wrapper


class ResourceOutline:

    def __init__(
        self,
        name: str,
        path: Optional[str] = None,
        icon: Optional[Image.Image] = None,
        uuid: Optional[UUID] = None,
        description: Optional[str] = None,
    ):
        self.name = name
        self.path = path
        self.icon = icon
        self.uuid = uuid
        self.description = description

    def __hash__(self) -> int:
        return hash(self.path)

    @staticmethod
    def is_pack(path: str, verbose: bool = False) -> bool:
        try:
            with BasePack.open(path, load_resources=False):
                return True
        except Exception as err:
            if verbose:
                pack = os.path.basename(path)
                print(f'"{pack}" failed: ', err)
            return False

    @staticmethod
    def from_pack(pack: "BasePack") -> "ResourceOutline":
        return ResourceOutline(
            name=pack.name,
            path=pack.filepath,
            icon=pack.get_pack_icon(),
            uuid=pack.uuid,
            description=pack.description,
        )

    @staticmethod
    def from_world(path: str) -> "ResourceOutline":
        img = Image.open(os.path.join(path, "world_icon.jpeg"))
        level = LevelFile.open(os.path.join(path, "level.dat"))

        def gm_to_name(gameType: int):
            match (gameType):
                case 0:
                    return "Survival"
                case 1:
                    return "Creative"
                case 2:
                    return "Adventure"
                case 5:
                    return "Survival"
                case 6:
                    return "Spectator"

        gm = gm_to_name(level.GameType)
        date = level.LastPlayed.strftime("%m/%d/%Y")
        size = get_folder_size(path)
        return ResourceOutline(
            name=level.LevelName,
            path=path,
            icon=img,
            description=f"{gm} - {date} - {size:.1f} MB",
        )

    @staticmethod
    def from_path(path: str) -> "ResourceOutline":
        # world
        level = os.path.join(path, "level.dat")
        if os.path.isfile(level):
            return ResourceOutline.from_world(path)

        # pack
        manifest = os.path.join(path, "manifest.json")
        if os.path.isfile(manifest):
            pack = BasePack.open(path)
            return ResourceOutline.from_pack(pack)

        # generic
        size = get_folder_size(path)
        return ResourceOutline(
            name=os.path.basename(path), path=path, description=f"{size:.1f} MB"
        )

    @staticmethod
    def find_packs(
        path: str, recursive: bool = False, verbose: bool = False
    ) -> Generator["ResourceOutline", Any, Any]:
        """
        Find all packs in PATH.

        :param path: The directory to search for packs.
        :type path: str
        :param recursive: When true it will search folders inside PATH for packs, defaults to False
        :type recursive: bool, optional
        :param verbose: Prints errors, defaults to False
        :type verbose: bool, optional
        :rtype: Generator[PackOutline, Any, Any]
        """
        root_dir = os.path.realpath(path)
        for fn in glob.glob("**/manifest.json", root_dir=root_dir, recursive=recursive):
            fp = os.path.dirname(os.path.join(root_dir, fn))
            if ResourceOutline.is_pack(fp, verbose):
                yield ResourceOutline.from_path(fp)


class Definition(dict[str, str]):
    def __init__(self, name: str):
        self.name = name


class BasePack(ABC, dict[str, File]):
    extension = ".mcpack"
    loaders: Dict[str, set[Type[File]]] = {}
    default_locale: str = "en_US"

    def __init__(self, manifest: Manifest):
        self.manifest = manifest

    def definitions(self) -> Dict[str, Definition]:
        result: Dict[str, Definition] = {}
        for fp, file in self.items():
            if isinstance(file, ResourceFile):
                if file.TYPE_ID not in result:
                    result[file.TYPE_ID] = Definition(name=file.TYPE_ID)
                result[file.TYPE_ID][fp] = file.id
        return result

    def find(self, filename_or_id: str) -> Optional[File]:
        # find by filename
        file = self.get(filename_or_id)
        if file:
            return file

        # find by id
        for x in self.definitions().values():
            for fp, id in x.items():
                if id == filename_or_id:
                    return self.get(fp)
        return None

    @property
    def filepath(self) -> Optional[str]:
        return getattr(self, "_filepath", None)

    @property
    def mode(self) -> str:
        return getattr(self, "_mode", "r")

    @property
    def format(self) -> str:
        return getattr(self, "_format", "zip")

    @property
    def name(self) -> str:
        k = self.manifest.header.name
        res = self.get(f"texts/{self.default_locale}.lang")
        if res is None:
            return k if k else "pack.name"
        return str(res.translate(k))  # type: ignore

    @property
    def description(self) -> str:
        k = self.manifest.header.description
        res = self.get(f"texts/{self.default_locale}.lang")
        if res is None:
            return k if k else "pack.description"
        return str(res.translate(k))  # type: ignore

    @property
    def uuid(self) -> UUID:
        return self.manifest.header.uuid

    @property
    def version(self) -> List[int]:
        return self.manifest.header.version

    @classmethod
    def add_loader(cls, file: Type[File], start_path: str = ".") -> None:
        if start_path not in cls.loaders:
            setattr(file, "_startpath", start_path)
            cls.loaders[start_path] = set([file])
            return

        cls.loaders[start_path].add(file)

    @classmethod
    def open(
        cls, file: str | Path, mode: str = "r", load_resources: bool = True
    ) -> Self:
        if "r" in mode:
            self = cls.load(file, load_resources)
            setattr(self, "_filepath", file)
            setattr(self, "_mode", mode)
            return self
        return cls.__new__(cls)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, a, b, c):
        if self.filepath is not None and "w" in self.mode:
            self.save(self.filepath)

    # TODO:
    def verify(self): ...

    def _load_resources(self, file: str | Path) -> Dict[str, File]:
        resources = {}
        for start, loaders in self.loaders.items():
            for loader in loaders:
                resource_path = os.path.join(file, start)
                if not os.path.exists(resource_path):
                    continue
                for path, sub_dirs, files in os.walk(resource_path):
                    for fn in files:
                        file_path = os.path.join(path, fn)
                        ext = os.path.splitext(file_path)[1]
                        if ext != loader.extension:
                            continue
                        id = os.path.relpath(file_path, file).replace("\\", "/")
                        try:
                            res = loader.open(file_path)
                        except Exception as err:
                            print(
                                f'Failed to parse {loader.__class__.__name__} in "{file_path}"'
                            )
                            raise err
                        resources[id] = res
        return resources

    def _load_languages(self, file: str | Path):
        fp = os.path.join(file, "texts", "languages.json")

        if not os.path.isfile(fp):
            return

        # TODO: Use computer locale
        with open(fp) as fd:
            data = commentjson.load(fd)
            if self.default_locale not in data:
                self.default_locale = data[0]

    @classmethod
    def load_directory(cls, file: str | Path, load_resources: bool = True) -> Self:
        self = cls.__new__(cls)

        # Load manifest
        fp = os.path.join(file, "manifest.json")
        if not os.path.isfile(fp):
            raise FileNotFoundError("manifest.json")
        self.manifest = Manifest.open(fp)
        self["manifest.json"] = self.manifest

        # Load resources
        if load_resources:
            self.update(self._load_resources(file))

        # Load default languages
        self._load_languages(file)
        return self

    # TODO
    @classmethod
    def load_zip(cls, file: str | Path, load_resources: bool = True) -> Self:
        print("LOAD ZIP")
        self = cls.__new__(cls)

        with zipfile.ZipFile(file) as zip:
            # TODO: get manifest.json
            print(zip)

        return self

    @classmethod
    def load(cls, file: str | Path, load_resources: bool = True) -> Self:
        if os.path.isfile(file):
            self = cls.load_zip(file, load_resources)
            setattr(self, "_format", "zip")
            return self
        self = cls.load_directory(file, load_resources)
        setattr(self, "_format", "directory")
        return self

    def save_zip(self, file: str) -> None:
        print("SAVE ZIP")

    def save_directory(self, file: str) -> None:
        print("SAVE DIR")

    def save(self, file: str, format: Optional[str] = None) -> None:
        format = self.format if format is None else format
        match format.lower():
            case "zip":
                self.save_zip(file)

            case "directory":
                self.save_directory(file)

    def get_pack_icon(self) -> Optional[Image.Image]:
        if self.filepath is None:
            return None
        fp = os.path.join(self.filepath, "pack_icon.png")
        if not os.path.isfile(fp):
            return None
        return Image.open(fp)


class ResourcePack(BasePack):
    loaders: Dict[str, set[Type[File]]] = {}


class BehaviorPack(BasePack):
    loaders: Dict[str, set[Type[File]]] = {}


class SkinPack(BasePack):
    loaders: Dict[str, set[Type[File]]] = {}
