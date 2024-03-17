from typing import Self
from zipfile import ZIP_DEFLATED, ZipFile
from multiprocessing import Pool
from io import BytesIO
import mclang
import os
import glob
import json


from . import VERSION
from .exception import ManifestNotFoundError
from .constant import Edition
from .manifest import Manifest
from .file import ArchiveFile, File, Importable
from .util import (
    getattr2,
    getitem,
    additem,
    clearitems,
    Identifier,
    Identifiable,
)
from .registry import INSTANCE, Registries, RegistryKey


# TODO: Instead of creating self.items, self.blocks, etc. add self.registry = {'item': RegistryKey()}
class Pack(ArchiveFile, Importable):
    def __init__(
        self, manifest: Manifest = None, texts: mclang.Lang = None, filename: str = None
    ):
        self.manifest = manifest
        self.texts = texts
        if filename:
            self.filename = filename

        self._methods = []

    def __getstate__(self):
        state = self.__dict__.copy()
        for m in self._methods:
            del state[m]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.__class__.__name__ + "{" + str(self.manifest.header.uuid) + "}"

    def __iter__(self):
        for reg in self.registry.keys():
            for obj in getattr(self, reg.path + "s"):
                yield obj

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier.of(value))

    @property
    def registry(self) -> RegistryKey:
        return getattr(self, "_registry")

    @registry.setter
    def registry(self, value: RegistryKey):
        if not isinstance(value, RegistryKey):
            raise TypeError(
                f"Expected RegistryKey but got '{value.__class__.__name__}' instead"
            )
        self.on_update("registry", value)
        setattr(self, "_registry", value)

    @property
    def manifest(self) -> Manifest:
        return getattr(self, "_manifest", self.MANIFEST)

    @manifest.setter
    def manifest(self, value: Manifest):
        if value is None:
            self.manifest = self.MANIFEST
            return
        if not isinstance(value, Manifest):
            raise TypeError(
                f"Expected Manifest but got '{value.__class__.__name__}' instead"
            )
        self.on_update("manifest", value)
        setattr(self, "_manifest", value)

    @property
    def texts(self) -> mclang.Lang:
        return getattr2(self, "_texts", mclang.Lang())

    @texts.setter
    def texts(self, value: mclang.Lang):
        if value is None:
            self.texts = mclang.Lang()
            return
        if not isinstance(value, mclang.Lang):
            raise TypeError(
                f"Expected mclang.Lang but got '{value.__class__.__name__}' instead"
            )
        self.on_update("texts", value)
        setattr(self, "_texts", value)

    @property
    def suffix(self) -> str:
        return getattr(self, "_suffix", "")

    @suffix.setter
    def suffix(self, value: str):
        if value is None:
            self.suffix = ""
            return
        setattr(self, "_suffix", str(value))

    # SHORTCUTS

    @property
    def name(self) -> str:
        return self.manifest.name

    @name.setter
    def name(self, value: str):
        self.on_update("name", value)
        self.manifest.name = value

    @property
    def description(self) -> str:
        return self.manifest.description

    @description.setter
    def description(self, value: str):
        self.on_update("description", value)
        self.manifest.description = value

    @property
    def versions(self) -> list[int]:
        return self.manifest.header.version

    @versions.setter
    def versions(self, value: list[int]):
        self.on_update("versions", value)
        self.manifest.header.version = value
        for m in self.manifest.modules:
            m.version = value

    @classmethod
    def load_archive(cls, zip: ZipFile) -> Self:
        self = cls.__new__(cls)
        self._create_file_methods()
        return ArchiveFile.load_archive(zip)

    @classmethod
    def load_directory(cls, path: str) -> Self:
        self = cls.__new__(cls)
        self._create_file_methods()
        manifest_path = os.path.join(path, "manifest.json")
        if not os.path.isfile(manifest_path):
            raise ManifestNotFoundError(manifest_path)

        # Load Manifest
        self.manifest = Manifest.open(manifest_path)

        # Load registry files
        for k, cls in self.registry.items():
            obj = cls.__new__(cls)
            start = os.path.join(path, obj.dirname)
            if os.path.isdir(start):
                for fp in glob.glob(start + "/**/*" + obj.extension, recursive=True):
                    bl = obj.valid(fp)
                    if bl:
                        file = obj.open(fp, start)
                        self.add(file)

        return self

    def _create_file_methods(self):
        self._methods = []
        for id in self.registry.keys():
            name = id.path
            objects = name + "s"
            if not hasattr(self, objects):
                setattr(self, objects, {})
            setattr(self, "get_" + name, lambda i, l=objects: self._get_file(l, i))
            setattr(
                self,
                "add_" + name,
                lambda obj, l=objects: self._add_file(l, obj),
            )
            setattr(
                self,
                "remove_" + name,
                lambda i, l=objects: self._remove_file(l, i),
            )
            setattr(self, f"clear_{name}s", lambda l=objects: self._clear_files(l))

            self._methods.extend(
                ["get_" + name, "add_" + name, "remove_" + name, f"clear_{name}s"]
            )

    def dump_directory(self, path: str, indent: int = 2) -> None:
        props = {"indent": indent}

        # MANIFEST
        fp = os.path.join(path, "manifest.json")
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w") as f:
            f.write(self.manifest.dumps(**props))

        # TEXTS
        name_key = self.manifest.header.name_key
        if name_key not in self.texts:
            self.texts[name_key] = self.manifest.name
        desc_key = self.manifest.header.description_key
        if desc_key not in self.texts:
            self.texts[desc_key] = self.manifest.description

        fp = os.path.join(path, "texts", "en_US.lang")
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w") as f:
            mclang.dump(self.texts, f)

        # LANGUAGES.json
        fp = os.path.join(path, "texts", "languages.json")
        with open(fp, "w") as w:
            json.dump(["en_US"], w)

        # FILES
        for k, cls in self.registry.items():
            obj = cls.__new__(cls)
            v = getattr(self, k.path + "s", {})
            if len(v) >= 1:
                dirpath = os.path.join(path, obj.dirname)
                os.makedirs(dirpath, exist_ok=True)
                for id, itm in v.items():
                    fp = os.path.join(dirpath, itm.filename + itm.extension)
                    fp_dir = os.path.dirname(fp)
                    if dirpath != fp_dir:
                        os.makedirs(fp_dir, exist_ok=True)
                    with open(fp, "w") as f:
                        f.write(itm.dumps(**props))

    def dump_archive(self, zip: ZipFile) -> None:
        if not isinstance(zip, ZipFile):
            raise TypeError(
                f"Expected zipfile.ZipFile but got '{zip.__class__.__name__}' instead"
            )
        props = {"separators": (",", ":")}
        path = ""

        # MANIFEST
        zip.writestr(os.path.join(path, "manfiest.json"), self.manifest.getvalue())

        # TEXTS
        name_key = self.manifest.header.name_key
        if name_key not in self.texts:
            self.texts[name_key] = self.manifest.name
        desc_key = self.manifest.header.description_key
        if desc_key not in self.texts:
            self.texts[desc_key] = self.manifest.description
        zip.writestr(
            os.path.join(path, "texts", "en_US.lang"), mclang.dumps(self.texts)
        )

        # LANGUAGES.json
        zip.writestr(
            os.path.join(path, "texts", "languages.json"), json.dumps(["en_US"])
        )

        # FILES
        for k, cls in self.registry.items():
            obj = cls.__new__(cls)
            v = getattr(self, k.path + "s", {})
            if len(v) >= 1:
                dirpath = os.path.join(path, obj.dirname)
                for id, itm in v.items():
                    fp = os.path.join(dirpath, itm.filename + itm.extension)
                    zip.writestr(fp, itm.getvalue())
                    # with open(fp, "w") as f:
                    #     f.write(itm.dumps(**props))
        return self

    def get_registry(self, registry: Identifiable):
        path = Identifiable.of(registry).path + "s"
        return getattr(self, path)

    def add(self, obj) -> Self:
        """
        Add File to this pack

        :param obj: The file to add
        :type obj: File
        """
        for cls in self.registry:
            if isinstance(obj, cls):
                name = cls.id.path + "s"
                getattr(self, name)[obj.identifier] = obj
                obj.generate(self)
                return self

    def set_details(self, name: str, description: str) -> Self:
        self.name = name
        self.description = description
        return self

    def _get_file(self, dirname: str, id: Identifiable) -> File:
        return getattr(self, dirname).get(Identifiable.of(id))

    def _add_file(self, dirname: str, obj: File) -> File:
        getattr(self, dirname)[obj.identifier] = obj
        return obj

    def _remove_file(self, dirname: str, id: Identifiable) -> File:
        return getattr(self, dirname).pop(Identifiable.of(id))

    def _clear_files(self, dirname: str) -> Self:
        setattr(self, dirname, {})
        return self

    def set_uuids(self, header_uuid: str, *module_uuid: str) -> Self:
        if self.manifest:
            self.manifest.set_uuids(header_uuid, *module_uuid)
        return self


INSTANCE.create_registry(Registries.BEHAVIOR_PACK_FILE, File)


def behavior_pack(cls):
    """
    Add this behavior pack file to the registry
    """

    def wrapper():
        if not issubclass(cls, File):
            raise TypeError(f"Expected File but got '{cls.__name__}' instead")
        return INSTANCE.register(Registries.BEHAVIOR_PACK_FILE, cls.id, cls)

    return wrapper()


class BehaviorPack(Pack):
    """
    Represents a Behavior Pack.
    """

    registry = INSTANCE.get_registry(Registries.BEHAVIOR_PACK_FILE)
    id = Identifier("data")
    FILEPATH = "behavior_packs/untitled.mcpack"
    suffix = "_BP"

    def __init__(
        self, manifest: Manifest = None, texts: mclang.Lang = None, filename: str = None
    ):
        Pack.__init__(self, manifest, texts, filename)
        self._create_file_methods()

    @property
    def MANIFEST(self):
        return getattr2(self, "_MANIFEST", Manifest.behavior())

    # UTIL

    def merge(self, other) -> Self:
        if not isinstance(other, self.__class__):
            raise TypeError(
                f"Expected {self.__class__.__name__} but got '{other.__class__.__name__}' instead"
            )
        self.items.update(other.items)
        self.blocks.update(other.blocks)
        self.recipes.update(other.recipes)
        return self

    # FILE

    def import_to(
        self, name: str = None, edition: Edition = Edition.BEDROCK, dev: bool = True
    ) -> str:
        mojang = super().import_to(name, edition, dev)
        dirpath = (
            os.path.join(mojang, "development_behavior_packs")
            if dev
            else os.path.join(mojang, "behavior_packs")
        )
        path = os.path.join(dirpath, self.filename + self.suffix)
        os.makedirs(path, exist_ok=True)
        self.save(path, zipped=False, overwrite=True)
        return path


INSTANCE.create_registry(Registries.RESOURCE_PACK_FILE, File)


def resource_pack(cls):
    """
    Add this resource pack file to the registry
    """

    def wrapper():
        if not issubclass(cls, File):
            raise TypeError(f"Expected File but got '{cls.__name__}' instead")
        return INSTANCE.register(Registries.RESOURCE_PACK_FILE, cls.id, cls)

    return wrapper()


class ResourcePack(Pack):
    """
    Represents a Resource Pack.
    """

    registry = INSTANCE.get_registry(Registries.RESOURCE_PACK_FILE)
    id = Identifier("resources")
    FILEPATH = "resource_packs/untitled.mcpack"
    suffix = "_RP"

    def __init__(
        self, manifest: Manifest = None, texts: mclang.Lang = None, filename: str = None
    ):
        Pack.__init__(self, manifest, texts, filename)
        self._create_file_methods()

    @property
    def MANIFEST(self):
        return getattr2(self, "_MANIFEST", Manifest.resource())

    # @classmethod
    # def open(cls, filename: str = None) -> Self:
    #     self = super().load(filename)
    #     self.filename = os.path.basename(filename)
    #     return self

    # UTIL

    def merge(self, other) -> Self:
        if not isinstance(other, self.__class__):
            raise TypeError(
                f"Expected {self.__class__.__name__} but got '{other.__class__.__name__}' instead"
            )
        return self

    # FILE

    @classmethod
    def load_archive(cls, zip: ZipFile) -> Self:
        self = cls.__new__(cls)
        self._create_file_methods()
        return self

    def dump_directory(self, path: str) -> None:
        props = {"indent": 2}

        v = getattr(self, "textures", {})
        for atlas_id, atlas in v.items():
            for id, textures in atlas.items():
                tpath = os.path.join(path, textures.dirname)
                os.makedirs(tpath, exist_ok=True)
                for t in textures:
                    fp = os.path.join(tpath, t.filename + t.extension)
                    t.save(fp)

        # Blocks
        if len(self.blocks) >= 1:
            fp = os.path.join(path, "blocks.json")
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            data = {"format_version": VERSION["BLOCKS"]}
            for id, block in self.blocks.items():
                b = {}
                if block.sound_group is not None:
                    b["sound"] = block.sound_group
                data[str(id)] = b

            with open(fp, "w") as fd:
                fd.write(json.dumps(data, **props))

        if hasattr(self, "clear_blocks"):
            self.clear_blocks()
        # self.clear_items()
        Pack.dump_directory(self, path)

    # TODO: Write blocks and items
    def dump_archive(self, zip: ZipFile) -> None:
        if hasattr(self, "clear_blocks"):
            self.clear_blocks()
        # self.clear_items()
        Pack.dump_archive(self, zip)

    def import_to(
        self, name: str = None, edition: Edition = Edition.BEDROCK, dev: bool = True
    ) -> str:
        mojang = super().import_to(name, edition, dev)
        dirpath = (
            os.path.join(mojang, "development_resource_packs")
            if dev
            else os.path.join(mojang, "resource_packs")
        )
        path = os.path.join(dirpath, self.filename + self.suffix)
        os.makedirs(path, exist_ok=True)
        self.save(path, zipped=False, overwrite=True)
        return path


def job(args):
    cls, manifest, pack_path = args
    if manifest.has_behavior():
        cls.add_pack(BehaviorPack.open(pack_path))
    elif manifest.has_resource():
        cls.add_pack(ResourcePack.open(pack_path))
    else:
        raise TypeError(f'Unknown pack type "{manifest}"')


class Addon(ArchiveFile, Importable):
    """
    Represents an Addon.
    """

    id = Identifier("addon")
    FILEPATH = "untitled.mcaddon"

    def __init__(self, filename: str = None):
        if filename is not None:
            self.filename = filename
        self.setup()

    def __iter__(self):
        for i in self.packs:
            yield i

    def __getitem__(self, item: Identifiable | int):
        if isinstance(item, int):
            return self.packs[item]
        id = Identifiable.of(item)
        for p in self.packs:
            if p.id == id:
                return p
        raise KeyError(repr(item))

    @classmethod
    def load(cls, filename: str = None) -> Self:
        self = super().load(filename)
        return self

    @property
    def packs(self) -> list[Pack]:
        return getattr2(self, "_packs", [])

    @packs.setter
    def packs(self, value: list[Pack]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("packs", value)
        setattr(self, "_packs", value)

    @property
    def manifests(self) -> list[Manifest]:
        return [p.manifest for p in self]

    @classmethod
    def load_archive(cls, zip: ZipFile, *args, **kw) -> Self:
        raise NotImplementedError()
        # self = cls.__new__(cls)
        # return self

    @classmethod
    def load_directory(cls, path: str, multiprocess: bool = False) -> Self:

        self = cls.__new__(cls)
        self.clear_packs()
        packs = [
            (self, Manifest.open(fp), os.path.dirname(fp))
            for fp in glob.glob(path + "/**/manifest.json")
        ]

        if multiprocess:
            # with Pool(20) as p:
            #     packs = p.map(job, packs)
            raise NotImplementedError("multiprocess not implemented yet!")
        else:
            for a in packs:
                job(a)
        return self

    def setup(self):
        # name = os.path.basename(self.filename)
        self.packs = [ResourcePack(), BehaviorPack()]

    def get(self, identifier: Identifiable, default=None):
        try:
            return self[Identifiable.of(identifier)]
        except (KeyError, IndexError):
            return default

    # PACK

    def append(self, pack: Pack) -> None:
        if not isinstance(pack, Pack):
            raise TypeError(
                f"Expected Pack but got '{pack.__class__.__name__}' instead"
            )
        self.packs.append(pack)

    def extend(self, packs: list[Pack]) -> None:
        self.packs.extend(packs)

    def get_pack(self, identifier: Identifiable) -> Pack | None:
        return getitem(self, "packs", Identifiable.of(identifier))

    def add_pack(self, pack: Pack) -> Pack:
        return additem(self, "packs", pack, type=Pack)

    def remove_pack(self, identifier: Identifiable) -> Pack:
        id = Identifiable.of(identifier)
        for i, p in enumerate(self.packs):
            if p.id == id:
                p2 = self.packs[i]
                del self.packs[i]
                return p2
        return None

    def clear_packs(self) -> Self:
        """Remove all packs"""
        return clearitems(self, "packs")

    def add(self, obj) -> File:
        """
        Add File to this addon

        :param obj: The file to add
        :type obj: File
        """
        try:
            for pack in self.packs:
                pack.add(obj)
        except TypeError as err:
            pass
        return obj

    # FILE

    def dump_directory(self, path: str) -> Self:
        for p in self.packs:
            p.dump_directory(
                os.path.join(path, os.path.basename(self.filename + p.suffix))
            )
        return self

    def dump_archive(self, zip: ZipFile) -> Self:
        for p in self.packs:
            file_buffer = BytesIO()
            with ZipFile(file_buffer, "a", ZIP_DEFLATED, False) as zip_file:
                p.dump_archive(zip_file)
            zip.writestr(
                (
                    self.filename + p.suffix + p.extension
                    if p.suffix != ""
                    else self.filename + p.extension
                ),
                file_buffer.getvalue(),
            )
        return self

    def import_to(
        self, name: str = None, edition: Edition = Edition.BEDROCK, dev: bool = True
    ) -> list[str]:
        return [pack.import_to(name, edition, dev) for pack in self]
