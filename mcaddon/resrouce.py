from typing import Self
from PIL import Image, ImageFile
import os

from .util import getattr2, Identifier, Identifiable
from .file import JsonFile, PngFile


class Texture(PngFile):
    """
    Represents a Texture.
    """

    FILENAME = "texture"
    EXTENSION = ".png"
    DIRNAME = "textures"

    def __init__(self, path: str, image: ImageFile.ImageFile):
        self.path = path
        self.image = image

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "Texture{" + repr(self.filename + self.extension) + "}"

    @property
    def __dict__(self) -> str:
        return os.path.join(
            "textures", self.path, self.filename + self.extension
        ).replace("\\", "/")

    @property
    def path(self) -> str:
        return getattr(self, "_path")

    @path.setter
    def path(self, value: str):
        setattr(self, "_path", str(value))

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
    def __init__(self, identifier: Identifier, textures: list[Texture]):
        Identifiable.__init__(self, identifier)
        self.textures = textures

    def __iter__(self):
        for t in self.textures:
            yield t

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "TextureDef{" + str(self.identifier) + "}"

    @property
    def __dict__(self) -> dict:
        data = {}
        if len(self.textures) == 1:
            data["textures"] = self.textures[0].__dict__
        else:
            data["textures"] = [t.__dict__ for t in self.textures]
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
        setattr(self, "_textures", value)


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
        identifier: Identifier,
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

    @property
    def __dict__(self) -> dict:
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
        setattr(self, "_atlas_tile", str(value))

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
        setattr(self, "_blend_frames", value)


class _Atlas(JsonFile):
    def __init__(
        self,
        resource_pack_name: str = None,
        texture_name: str = None,
        texture_data: dict[Identifier, dict] = None,
    ):
        self.resource_pack_name = resource_pack_name
        self.texture_name = texture_name
        self.texture_data = texture_data

    def __iter__(self):
        for t in self.texture_data.values():
            yield t

    @property
    def __dict__(self) -> dict:
        data = {
            "resource_pack_name": self.resource_pack_name,
            "texture_name": self.texture_name,
            "texture_data": {},
        }
        for k, v in self.texture_data.items():
            key = k.path if k.namespace == "minecraft" else k
            data["texture_data"][str(key)] = v.__dict__
        return data

    @property
    def resource_pack_name(self) -> str:
        return getattr(self, "_resource_pack_name", "vanilla")

    @resource_pack_name.setter
    def resource_pack_name(self, value: str):
        if value is None:
            self.resource_pack_name = "vanilla"
            return
        setattr(self, "_resource_pack_name", str(value))

    @property
    def texture_name(self) -> str:
        return getattr(self, "_texture_name", "atlas.terrain")

    @texture_name.setter
    def texture_name(self, value: str):
        if value is None:
            self.texture_name = "atlas.terrain"
            return
        setattr(self, "_texture_name", str(value))

    @property
    def texture_data(self) -> dict[Identifier, dict]:
        return getattr2(self, "_texture_data", {})

    @texture_data.setter
    def texture_data(self, value: dict[Identifier, dict]):
        if value is None:
            self.texture_data = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_texture_data", value)

    def get_texture(self, identifier: Identifier) -> dict | None:
        return self.texture_data.get(identifier)

    def add_texture(self, texture: _TextureDef) -> _TextureDef:
        if not isinstance(texture, _TextureDef):
            raise TypeError(
                f"Expected _TextureDef but got '{texture.__class__.__name__}' instead"
            )
        self.texture_data[texture.identifier] = texture
        return texture

    def remove_texture(self, identifier: Identifier) -> dict | None:
        return self.texture_data.pop(identifier)

    def clear_textures(self) -> Self:
        self.texture_data = {}
        return self

    def items(self):
        return self.texture_data.items()


class TerrainAtlas(_Atlas):
    """
    Represents a Terrain Textures Atlas.
    """

    identifier = Identifier("terrain_texture")
    FILENAME = "terrain_texture"
    EXTENSION = ".json"
    DIRNAME = "textures"

    def __init__(
        self,
        resource_pack_name: str = None,
        texture_name: str = None,
        padding: int = None,
        num_mip_levels: int = None,
        texture_data: dict[Identifier, dict] = None,
    ):
        _Atlas.__init__(self, resource_pack_name, texture_name, texture_data)
        self.padding = padding
        self.num_mip_levels = num_mip_levels

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        setattr(self, "_num_mip_levels", value)


class ItemAtlas(_Atlas):
    """
    Represents a Item Textures Atlas.
    """

    identifier = Identifier("item_texture")
    FILENAME = "item_texture"
    EXTENSION = ".json"
    DIRNAME = "textures"

    def __init__(
        self,
        resource_pack_name: str = None,
        texture_name: str = None,
        texture_data: dict[Identifier, dict] = None,
    ):
        _Atlas.__init__(self, resource_pack_name, texture_name, texture_data)

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        return data
