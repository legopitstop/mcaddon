from typing import Self
from zipfile import ZIP_DEFLATED, ZipFile
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
from .util import getattr2, Identifier
from .resrouce import ItemAtlas, TerrainAtlas
from .recipe import Recipe
from .block import Block
from .item import Item
from .volume import Volume
from .loot import LootTable


class Pack(Importable):
    def __init__(
        self, manifest: Manifest = None, texts: mclang.Lang = None, filename: str = None
    ):
        self.manifest = manifest
        self.texts = texts
        if filename:
            self.filename = filename

    def __str__(self) -> str:
        return self.__class__.__name__ + "{" + str(self.manifest.header.uuid) + "}"

    @property
    def file_types(self) -> list[File]:
        return getattr(self, "_file_types")

    @file_types.setter
    def file_types(self, value: list[File]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_file_types", value)

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
        self.manifest.name = value

    @property
    def description(self) -> str:
        return self.manifest.description

    @description.setter
    def description(self, value: str):
        self.manifest.description = value

    @property
    def versions(self) -> list[int]:
        return self.manifest.header.version

    @versions.setter
    def versions(self, value: list[int]):
        self.manifest.header.version = value
        for m in self.manifest.modules:
            m.version = value

    def _create_file_methods(self):
        for f in self.file_types:
            setattr(self, f.dirname, {})
            setattr(
                self, "get_" + f.filename, lambda i, l=f.dirname: self.get_file(l, i)
            )
            setattr(
                self,
                "add_" + f.filename,
                lambda obj, l=f.dirname: self.add_file(l, obj),
            )
            setattr(
                self,
                "remove_" + f.filename,
                lambda i, l=f.dirname: self.remove_file(l, i),
            )
            setattr(
                self, "clear_" + f.filename, lambda l=f.dirname: self.clear_files(l)
            )

    def set_details(self, name: str, description: str) -> Self:
        self.name = name
        self.description = description
        return self

    def get_file(self, dirname: str, id: Identifier) -> File:
        return getattr(self, dirname).get(id)

    def add_file(self, dirname: str, obj: File) -> File:
        getattr(self, dirname)[obj.identifier] = obj
        return obj

    def remove_file(self, dirname: str, id: Identifier) -> File:
        return getattr(self, dirname).pop(id)

    def clear_files(self, dirname: str) -> Self:
        setattr(self, dirname, {})
        return self

    def set_uuids(self, header_uuid: str, *module_uuid: str) -> Self:
        if self.manifest:
            self.manifest.set_uuids(header_uuid, *module_uuid)
        return self

    def writedir(self, path: str) -> None:
        props = {"indent": 2}

        # MANIFEST
        fp = os.path.join(path, "manifest.json")
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w") as f:
            f.write(self.manifest.json(**props))

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

        # FILES
        for k in self.file_types:
            v = getattr(self, k.dirname, {})
            if len(v) >= 1:
                dirpath = os.path.join(path, k.dirname)
                os.makedirs(dirpath, exist_ok=True)
                for id, itm in v.items():
                    fp = os.path.join(dirpath, itm.filename + itm.extension)
                    with open(fp, "w") as f:
                        f.write(itm.json(**props))

    def writezip(self, zip: ZipFile) -> None:
        props = {"separators": (",", ":")}
        path = ""

        # MANIFEST
        zip.writestr(os.path.join(path, "manfiest.json"), self.manifest.json(**props))

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

        # FILES
        # for k, v in self.files.items():
        #     dirpath = os.path.join(path, k)
        #     for id, itm in v.items():
        #         fp = os.path.join(dirpath, itm.filename+itm.EXT)
        #         zip.writestr(fp, itm.json(**props))

        for k in self.file_types:
            dirpath = os.path.join(path, k.dirname)
            v = getattr(self, k.dirname, {})
            for id, itm in v.items():
                fp = os.path.join(dirpath, itm.filename + itm.extension)
                zip.writestr(fp, itm.json(**props))
        return self


class BehaviorPack(ArchiveFile, Pack):
    """
    Represents a Behavior Pack.
    """

    id = Identifier("data")
    EXTENSION = ".mcpack"
    FILENAME = "untitled"
    DIRNAME = "behavior_packs"
    suffix = "_BP"

    def __init__(
        self, manifest: Manifest = None, texts: mclang.Lang = None, filename: str = None
    ):
        Pack.__init__(self, manifest, texts, filename)
        self.setup()

    @property
    def MANIFEST(self):
        return getattr2(self, "_MANIFEST", Manifest.behavior())

    @classmethod
    def load(cls, filename: str = None) -> Self:
        self = super().load(filename)
        return self

    def setup(self):
        self.file_types = [
            Item.__new__(Item),
            Block.__new__(Block),
            Recipe.__new__(Recipe),
            Volume.__new__(Volume),
            LootTable.__new__(LootTable),
        ]
        self._create_file_methods()

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

    def add(self, obj) -> Self:
        if isinstance(obj, Item):
            return self.add_item(obj)
        if isinstance(obj, Block):
            return self.add_block(obj)
        if isinstance(obj, Recipe):
            return self.add_recipe(obj)
        if isinstance(obj, Volume):
            return self.add_volume(obj)
        return self

    # FILE

    @classmethod
    def readzip(cls, zip: ZipFile) -> Self:
        self = cls.__new__(cls)
        self.setup()
        return self

    @classmethod
    def readdir(cls, path: str) -> Self:
        self = cls.__new__(cls)
        self.setup()
        manifest_path = os.path.join(path, "manifest.json")
        if not os.path.isfile(manifest_path):
            raise ManifestNotFoundError(manifest_path)

        for v in self.file_types:
            k_path = os.path.join(path, v.dirname)
            if os.path.isdir(k_path):
                for fp in glob.glob(k_path + "/**" + v.extension):
                    self.add_file(v.dirname, v.load(fp))

        return self

    def writedir(self, path: str) -> None:
        Pack.writedir(self, path)

    def writezip(self, zip: ZipFile) -> None:
        Pack.writezip(self, zip)

    def import_to(self, edition: Edition = Edition.bedrock, dev: bool = True) -> str:
        mojang = super().import_to(edition, dev)
        dirpath = (
            os.path.join(mojang, "development_behavior_packs")
            if dev
            else os.path.join(mojang, "behavior_packs")
        )
        path = os.path.join(dirpath, self.filename + self.suffix)
        os.makedirs(path, exist_ok=True)
        self.writedir(path)
        return path

    # RECIPE

    def get_recipe(self) -> Recipe | None: ...
    def add_recipe(self, recipe: Recipe) -> Recipe: ...
    def remove_recipe(self, identifier: Identifier | str) -> Recipe | None: ...
    def clear_recipes(self) -> Self: ...

    # BLOCK

    def get_block(self) -> Block | None: ...
    def add_block(self, block: Block) -> Block: ...
    def remove_block(self, identifier: Identifier | str) -> Block | None: ...
    def clear_blocks(self): ...

    # ITEM

    def get_item(self) -> Item | None: ...
    def add_item(self, item: Item) -> Item: ...
    def remove_item(self, identifier: Identifier | str) -> Item | None: ...
    def clear_items(self) -> Self: ...

    # VOLUME

    def get_volume(self) -> Volume | None: ...
    def add_volume(self, volume: Volume) -> Volume: ...
    def remove_volume(self, identifier: Identifier | str) -> Item | None: ...
    def clear_volumes(self) -> Self: ...


class ResourcePack(ArchiveFile, Pack):
    """
    Represents a Resource Pack.
    """

    id = Identifier("resources")
    EXTENSION = ".mcpack"
    FILENAME = "untitled"
    DIRNAME = "resource_packs"
    suffix = "_RP"

    def __init__(
        self, manifest: Manifest = None, texts: mclang.Lang = None, filename: str = None
    ):
        Pack.__init__(self, manifest, texts, filename)
        self.setup()

    @property
    def MANIFEST(self):
        return getattr2(self, "_MANIFEST", Manifest.resource())

    @property
    def blocks(self) -> dict[Identifier, Block]:
        return getattr2(self, "_blocks", {})

    @blocks.setter
    def blocks(self, value: dict[Identifier, Block]):
        if value is None:
            self.blocks = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_blocks", value)

    @property
    def items(self) -> dict[Identifier, Item]:
        return getattr2(self, "_items", {})

    @items.setter
    def items(self, value: dict[Identifier, Item]):
        if value is None:
            self.items = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_items", value)

    @classmethod
    def load(cls, filename: str = None) -> Self:
        self = super().load(filename)
        return self

    def setup(self):
        self.file_types = [
            ItemAtlas.__new__(ItemAtlas),
            TerrainAtlas.__new__(TerrainAtlas),
        ]
        self._create_file_methods()

    # UTIL

    def merge(self, other) -> Self:
        if not isinstance(other, self.__class__):
            raise TypeError(
                f"Expected {self.__class__.__name__} but got '{other.__class__.__name__}' instead"
            )
        return self

    # SHORTHAND

    def add(self, obj) -> Self:
        if isinstance(obj, ItemAtlas):
            return self.add_item_texture(obj)
        if isinstance(obj, TerrainAtlas):
            return self.add_terrain_texture(obj)
        raise TypeError(obj)

    # FILE

    @classmethod
    def readzip(cls, zip: ZipFile) -> Self:
        self = cls.__new__(cls)
        return self

    @classmethod
    def readdir(cls, path: str) -> Self:
        self = cls.__new__(cls)
        return self

    def writedir(self, path: str) -> None:
        Pack.writedir(self, path)
        props = {"indent": 2}

        v = getattr(self, "textures", {})
        for atlas_id, atlas in v.items():
            for id, textures in atlas.items():
                tpath = os.path.join(path, textures.dirname)
                os.makedirs(tpath, exist_ok=True)
                for t in textures:
                    fp = os.path.join(tpath, t.filename + t.extension)
                    t.save(fp)

        if len(self.blocks) >= 1:
            fp = os.path.join(path, "blocks.json")
            data = {"format_version": VERSION["BLOCKS"]}
            for id, block in self.blocks.items():
                b = {}
                if block.sound_group is not None:
                    b["sound"] = block.sound_group
                data[str(id)] = b

            with open(fp, "w") as fd:
                fd.write(json.dumps(data, **props))

    def writezip(self, zip: ZipFile) -> None:
        Pack.writezip(self, zip)

    def import_to(self, edition: Edition = Edition.bedrock, dev: bool = True) -> str:
        mojang = super().import_to(edition, dev)
        dirpath = (
            os.path.join(mojang, "development_resource_packs")
            if dev
            else os.path.join(mojang, "resource_packs")
        )
        path = os.path.join(dirpath, self.filename + self.suffix)
        os.makedirs(path, exist_ok=True)
        self.writedir(path)
        return path

    # BLOCK

    def get_block(self, identifier) -> Block | None:
        return self.blocks.get(identifier)

    def add_block(self, block: Block) -> Block:
        self.blocks[block.identifier] = block
        return block

    def remove_block(self, identifier: Block | str) -> Block | None:
        return self.blocks.pop(identifier)

    def clear_block(self) -> Self:
        self.blocks = {}
        return self

    # ITEM

    def get_item(self, identifier) -> Item | None:
        return self.items.get(identifier)

    def add_item(self, item: Item) -> Item:
        self.items[item.identifier] = item
        return item

    def remove_item(self, identifier: Item | str) -> Item | None:
        return self.items.pop(identifier)

    def clear_item(self) -> Self:
        self.items = {}
        return self

    # ITEM ATLAS

    def get_item_texture(self, identifier) -> ItemAtlas | None: ...
    def add_item_texture(self, atlas: ItemAtlas) -> ItemAtlas: ...
    def remove_item_texture(self, identifier: ItemAtlas | str) -> ItemAtlas | None: ...
    def clear_item_texture(self) -> Self: ...

    # TERRAIN ATLAS

    def get_terrain_texture(self, identifier) -> TerrainAtlas | None: ...
    def add_terrain_texture(self, atlas: TerrainAtlas) -> TerrainAtlas: ...
    def remove_terrain_texture(
        self, identifier: TerrainAtlas | str
    ) -> TerrainAtlas | None: ...
    def clear_terrain_texture(self) -> Self: ...


class Addon(ArchiveFile, Importable):
    """
    Represents an Addon.
    """

    id = Identifier("addon")
    EXTENSION = ".mcaddon"
    FILENAME = "untitled"

    def __init__(self):
        self.setup()

    def __iter__(self):
        for i in self.packs:
            yield i

    def __getitem__(self, item: Identifier | str | int):
        if isinstance(item, int):
            return self.packs[item]
        id = Identifier(item)
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
        setattr(self, "_packs", value)

    @property
    def manifests(self) -> list[Manifest]:
        return [p.manifest for p in self]

    @classmethod
    def readzip(cls, zip: ZipFile) -> Self:
        self = cls.__new__(cls)
        return self

    @classmethod
    def readdir(cls, path: str) -> Self:
        self = cls.__new__(cls)
        self.clear_packs()
        for fp in glob.glob(path + "/**/manifest.json"):
            manifest = Manifest.load(fp)
            pack_path = os.path.dirname(fp)

            # print(manifest.pack())
        return self

    def setup(self):
        # name = os.path.basename(self.filename)
        self.packs = [ResourcePack(), BehaviorPack()]

    def get(self, identifier: Identifier, default=None):
        try:
            return self[identifier]
        except (KeyError, IndexError):
            return default

    # PACK

    def get_pack(self, identifier: Identifier) -> Pack | None:
        return self.get(identifier)

    def add_pack(self, pack: Pack) -> Pack:
        if not isinstance(pack, Pack):
            raise TypeError(
                f"Expected Pack but got '{pack.__class__.__name__}' instead"
            )
        self.packs.append(pack)
        return pack

    def remove_pack(self, identifier: Identifier) -> Pack:
        for i, p in enumerate(self.packs):
            if p.id == identifier:
                p2 = self.packs[i]
                del self.packs[i]
                return p2
        return None

    def clear_packs(self) -> Self:
        self.packs = []
        return self

    # ADD

    def add(self, obj) -> Self:
        if isinstance(obj, Item):
            return self.add_item(obj)
        if isinstance(obj, Block):
            return self.add_block(obj)
        if isinstance(obj, Recipe):
            return self.add_recipe(obj)
        if isinstance(obj, Volume):
            return self.add_volume(obj)
        if isinstance(obj, LootTable):
            return self.add_loot_table(obj)
        if isinstance(obj, ItemAtlas):
            return self.add_item_texture(obj)
        if isinstance(obj, TerrainAtlas):
            return self.add_terrain_texture(obj)
        raise TypeError(obj)

    def add_recipe(self, recipe: Recipe) -> Recipe:
        self["data"].add_recipe(recipe)
        return recipe

    def add_block(self, block: Block) -> Block:
        self["data"].add_block(block)
        self["resources"].add_block(block)
        return block

    def add_item(self, item: Item) -> Item:
        self["data"].add_item(item)
        self["resources"].add_item(item)
        return item

    def add_volume(self, volume: Volume) -> Volume:
        self["data"].add_volume(volume)
        return volume

    def add_loot_table(self, loot_table: LootTable) -> LootTable:
        self["data"].add_loot_table(loot_table)
        return loot_table

    def add_item_texture(self, atlas: ItemAtlas) -> ItemAtlas:
        self["resources"].add_item_texture(atlas)
        return atlas

    def add_terrain_texture(self, atlas: TerrainAtlas) -> TerrainAtlas:
        self["resources"].add_terrain_texture(atlas)
        return atlas

    # FILE

    def writedir(self, path: str) -> Self:
        name = os.path.basename(path)
        for p in self.packs:
            filename = p.filename
            if not p.has_filename():
                filename = name + p.suffix
            p.writedir(os.path.join(path, os.path.basename(filename)))
        return self

    def writezip(self, zip: ZipFile) -> Self:
        for p in self.packs:
            file_buffer = BytesIO()
            with ZipFile(file_buffer, "a", ZIP_DEFLATED, False) as zip_file:
                p.writezip(zip_file)
            fp = os.path.basename(p.filename)
            if p.suffix != "":
                fp += p.suffix
            zip.writestr(fp + ".mcpack", file_buffer.getvalue())
        return self

    def import_to(
        self, edition: Edition = Edition.bedrock, dev: bool = True
    ) -> list[str]:
        return [pack.import_to(edition, dev) for pack in self]
