__all__ = ["TextureFile", "TextureSet"]

from pathlib import Path
from typing import Tuple, Optional
from io import BytesIO
from PIL import ImageFile, Image

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from mcaddon.core.file import BinaryFile, ResourceFile
from .pack import resourcepack

ImageFile.LOAD_TRUNCATED_IMAGES = True


# TODO:
# - Add additional props, E.g; texture set.
@resourcepack("textures")
class TextureFile(BinaryFile):
    extension = ".png"

    def __init__(self, source: ImageFile.ImageFile):
        self.source = source

    @property
    def id(self) -> str:
        if not self.filepath or not self.startpath:
            return "empty"

        parts = Path(self.filepath).parts
        idx = parts.index(self.startpath)
        return str(Path(*parts[idx:]))

    @classmethod
    def loads(cls, obj: bytes, *args, **kw) -> Self:
        self = cls.__new__(cls)
        self.source = Image.open(BytesIO(obj), formats=["png", "jpeg", "tga"])
        return self

    def dumps(self, *args, **kw) -> bytes:
        io = BytesIO()
        self.source.save(io)
        return io.getvalue()

    def show(self):
        self.source.show()


_Color = str | Tuple[int, int, int, int]


@resourcepack("textures")
class TextureSet(ResourceFile):
    extension = ".texture_set.json"
    TYPE_ID = "minecraft:texture_set"

    color: _Color
    normal: Optional[_Color] = None
    heightmap: Optional[_Color] = None
    metalness_emissive_roughness: Optional[_Color] = None
