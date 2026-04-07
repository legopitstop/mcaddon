__all__ = ["SpawnRuleSpawnsLava"]


from .component import SpawnRuleComponent
from typing import ClassVar


@SpawnRuleComponent.register
class SpawnRuleSpawnsLava(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_lava)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:spawns_lava"
