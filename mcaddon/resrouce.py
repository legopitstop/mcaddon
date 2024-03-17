from typing import Self
from PIL import Image, ImageFile
import os

from .util import (
    getattr2,
    getitem,
    additem,
    removeitem,
    clearitems,
    Identifier,
    Identifiable,
)
from .file import JsonFile, PngFile
from .pack import resource_pack


class Texture(PngFile):
    """
    Represents a Texture.
    """

    id = Identifier("texture")
    FILEPATH = "textures/texture.png"

    def __init__(self, path: str, image: ImageFile.ImageFile):
        self.path = path
        self.image = image

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "Texture{" + repr(self.filename + self.extension) + "}"

    def jsonify(self) -> str:
        return os.path.join(
            "textures", self.path, self.filename + self.extension
        ).replace("\\", "/")

    @property
    def path(self) -> str:
        return getattr(self, "_path")

    @path.setter
    def path(self, value: str):
        v = str(value)
        self.on_update("path", v)
        setattr(self, "_path", v)

    @classmethod
    def load(cls, filename: str, path: str) -> Self:
        self = cls.__new__(cls)
        self.image = Image.open(filename)
        self.filename, ext = os.path.splitext(os.path.basename(self.image.filename))
        self.path = path
        return self

    def save(self, fp: str):
        self.image.save(fp)


class _TextureDef(Identifiable):
    def __init__(self, identifier: Identifiable, textures: list[Texture]):
        Identifiable.__init__(self, identifier)
        self.textures = textures

    def __iter__(self):
        for t in self.textures:
            yield t

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "TextureDef{" + str(self.identifier) + "}"

    def jsonify(self) -> dict:
        data = {}
        if len(self.textures) == 1:
            data["textures"] = self.textures[0].jsonify()
        else:
            data["textures"] = [t.jsonify() for t in self.textures]
        return data

    @property
    def textures(self) -> list[Texture]:
        return getattr(self, "_textures")

    @textures.setter
    def textures(self, value: list[Texture]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("textures", value)
        setattr(self, "_textures", value)

    def get_texture(self, index: int) -> Texture:
        return getitem(self, "textures", index)

    def add_texture(self, texture: Texture) -> Texture:
        return additem(self, "textures", texture, type=Texture)

    def remove_texture(self, index: int) -> Texture:
        return removeitem(self, "textures", index)

    def clear_textures(self) -> Self:
        """Remove all textures"""
        return clearitems(self, "textures")


class ItemTexture(_TextureDef):
    """
    Represents an Item Texture.
    """

    dirname = "textures\\items"


class TerrainTexture(_TextureDef):
    """
    Represents a Terrain Texture.
    """

    dirname = "textures\\blocks"


class FlipbookTexture(Identifiable):
    """
    Represents a Flipbook Texture.
    """

    def __init__(
        self,
        identifier: Identifiable,
        flipbook_texture: Texture,
        atlas_tile: int = None,
        atlas_index: int = None,
        atlas_tile_variant: int = None,
        ticks_per_frame: int = None,
        frames: list[int] | int = None,
        replicate: int = None,
        blend_frames: bool = None,
    ):
        Identifiable.__init__(self, identifier)
        self.flipbook_texture = flipbook_texture
        self.atlas_tile = atlas_tile
        self.atlas_index = atlas_index
        self.atlas_tile_variant = atlas_tile_variant
        self.ticks_per_frame = ticks_per_frame
        self.frames = frames
        self.replicate = replicate
        self.blend_frames = blend_frames

    def jsonify(self) -> dict:
        data = {"flipbook_texture": self.flipbook_texture.path}
        if self.atlas_tile:
            data["atlas_tile"] = self.atlas_tile
        if self.atlas_index:
            data["atlas_index"] = self.atlas_index
        if self.atlas_tile_variant:
            data["atlas_tile_variant"] = self.atlas_tile_variant
        if self.ticks_per_frame:
            data["ticks_per_frame"] = self.ticks_per_frame
        if self.frames:
            data["frames"] = self.frames
        if self.replicate not in [None, 1]:
            data["replicate"] = self.replicate
        if self.blend_frames not in [None, True]:
            data["blend_frames"] = self.blend_frames
        return data

    @property
    def atlas_tile(self) -> str:
        return getattr(self, "_atlas_tile", None)

    @atlas_tile.setter
    def atlas_tile(self, value: str):
        if value is None:
            setattr(self, "_atlas_tile", None)
            return
        v = str(value)
        self.on_update("atlas_tile", v)
        setattr(self, "_atlas_tile", v)

    @property
    def atlas_index(self) -> int:
        return getattr(self, "_atlas_index", None)

    @atlas_index.setter
    def atlas_index(self, value: int):
        if value is None:
            setattr(self, "_atlas_index", None)
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("atlas_index", value)
        setattr(self, "_atlas_index", value)

    @property
    def atlas_tile_variant(self) -> int:
        return getattr(self, "_atlas_tile_variant", None)

    @atlas_tile_variant.setter
    def atlas_tile_variant(self, value: int):
        if value is None:
            setattr(self, "_atlas_tile_variant", None)
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("atlas_tile_variant", value)
        setattr(self, "_atlas_tile_variant", value)

    @property
    def ticks_per_frame(self) -> int:
        return getattr(self, "_ticks_per_frame", None)

    @ticks_per_frame.setter
    def ticks_per_frame(self, value: int):
        if value is None:
            setattr(self, "_ticks_per_frame", None)
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("ticks_per_frame", value)
        setattr(self, "_ticks_per_frame", value)

    @property
    def frames(self) -> list[int]:
        return getattr(self, "_frames", None)

    @frames.setter
    def frames(self, value: list[int]):
        if value is None:
            setattr(self, "_frames", None)
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("frames", value)
        setattr(self, "_frames", value)

    @property
    def replicate(self) -> int:
        return getattr(self, "_replicate", 1)

    @replicate.setter
    def replicate(self, value: int):
        if value is None:
            self.replicate = 1
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("replicate", value)
        setattr(self, "_replicate", value)

    @property
    def blend_frames(self) -> bool:
        return getattr(self, "_blend_frames", True)

    @blend_frames.setter
    def blend_frames(self, value: bool):
        if value is None:
            self.blend_frames = True
            return
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("blend_frames", value)
        setattr(self, "_blend_frames", value)


class _Atlas(JsonFile):
    def __init__(
        self,
        resource_pack_name: str = None,
        texture_name: str = None,
        texture_data: dict[Identifiable, dict] = None,
    ):
        self.resource_pack_name = resource_pack_name
        self.texture_name = texture_name
        self.texture_data = texture_data

    def __iter__(self):
        for t in self.texture_data.values():
            yield t

    def jsonify(self) -> dict:
        data = {
            "resource_pack_name": self.resource_pack_name,
            "texture_name": self.texture_name,
            "texture_data": {},
        }
        for k, v in self.texture_data.items():
            key = k.path if k.namespace == "minecraft" else k
            data["texture_data"][str(key)] = v.jsonify()
        return data

    @property
    def resource_pack_name(self) -> str:
        return getattr(self, "_resource_pack_name", "vanilla")

    @resource_pack_name.setter
    def resource_pack_name(self, value: str):
        if value is None:
            self.resource_pack_name = "vanilla"
            return
        v = str(value)
        self.on_update("resource_pack_name", v)
        setattr(self, "_resource_pack_name", v)

    @property
    def texture_name(self) -> str:
        return getattr(self, "_texture_name", "atlas.terrain")

    @texture_name.setter
    def texture_name(self, value: str):
        if value is None:
            self.texture_name = "atlas.terrain"
            return
        v = str(value)
        self.on_update("texture_name", v)
        setattr(self, "_texture_name", v)

    @property
    def texture_data(self) -> dict[Identifier, dict]:
        return getattr2(self, "_texture_data", {})

    @texture_data.setter
    def texture_data(self, value: dict[Identifiable, dict]):
        if value is None:
            self.texture_data = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        data = {}
        for k, v in value.items():
            data[Identifiable.of(k)] = v
        self.on_update("texture_data", data)
        setattr(self, "_texture_data", data)

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier.of(value))

    def get_texture_data(self, identifier: Identifiable) -> dict | None:
        return getitem(self, "texture_data", Identifiable.of(identifier))

    def add_texture_data(self, texture: _TextureDef) -> _TextureDef:
        return additem(self, "texture_data", texture, texture.identifier)

    def remove_texture_data(self, texture: Identifiable) -> dict | None:
        return removeitem(self, "texture_data", Identifiable.of(texture))

    def clear_texture_data(self) -> Self:
        return clearitems(self, "texture_data")

    def items(self):
        return self.texture_data.items()


@resource_pack
class TerrainAtlas(_Atlas):
    """
    Represents a Terrain Textures Atlas.
    """

    id = Identifier("terrain_texture")
    FILEPATH = "textures/terrain_texture.json"

    def __init__(
        self,
        resource_pack_name: str = None,
        texture_name: str = None,
        padding: int = None,
        num_mip_levels: int = None,
        texture_data: dict[Identifiable, dict] = None,
    ):
        _Atlas.__init__(self, resource_pack_name, texture_name, texture_data)
        self.padding = padding
        self.num_mip_levels = num_mip_levels

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["padding"] = self.padding
        data["num_mip_levels"] = self.num_mip_levels
        return data

    @property
    def padding(self) -> int:
        return getattr(self, "_padding", 8)

    @padding.setter
    def padding(self, value: int):
        if value is None:
            self.padding = 8
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("padding", value)
        setattr(self, "_padding", value)

    @property
    def num_mip_levels(self) -> int:
        return getattr(self, "_num_mip_levels", 4)

    @num_mip_levels.setter
    def num_mip_levels(self, value: int):
        if value is None:
            self.num_mip_levels = 4
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("num_mip_levels", value)
        setattr(self, "_num_mip_levels", value)


@resource_pack
class ItemAtlas(_Atlas):
    """
    Represents a Item Textures Atlas.
    """

    id = Identifier("item_texture")
    FILEPATH = "textures/item_texture.json"

    def __init__(
        self,
        resource_pack_name: str = None,
        texture_name: str = None,
        texture_data: dict[Identifiable, dict] = None,
    ):
        _Atlas.__init__(self, resource_pack_name, texture_name, texture_data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        return data
