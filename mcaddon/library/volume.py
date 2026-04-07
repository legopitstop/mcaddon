__all__ = ["Volume"]

from mcaddon.core.file import ResourceFile
from .pack import behaviorpack


@behaviorpack("loot_tables")
class Volume(ResourceFile):
    TYPE_ID = "minecraft:volume"
