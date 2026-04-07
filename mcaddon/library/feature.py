__all__ = ["AggregateFeature"]

from mcaddon.core.file import ResourceFile
from .pack import behaviorpack


@behaviorpack("features")
class AggregateFeature(ResourceFile):
    TYPE_ID = "minecraft:aggregate_feature"
