__all__ = ["Camera"]

from mcaddon.core.file import ResourceFile
from .pack import behaviorpack


@behaviorpack("loot_tables")
class Camera(ResourceFile):
    TYPE_ID = "minecraft:camera"
