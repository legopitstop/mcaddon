__all__ = ["FeatureRule"]

from mcaddon.core.file import ResourceFile
from .pack import behaviorpack


@behaviorpack("feature_rules")
class FeatureRule(ResourceFile):
    TYPE_ID = "minecraft:feature_rule"
