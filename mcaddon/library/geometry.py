__all__ = ["Geometries", "Geometry"]


from mcaddon.core.base import BaseModel
from mcaddon.core.file import ResourceFile
from .pack import resourcepack


class Geometry(BaseModel):
    pass


@resourcepack("models/entity")
@resourcepack("models/block")
class Geometries(ResourceFile):
    TYPE_ID = "minecraft:geometry"

    format_version: str = "1.16.0"
