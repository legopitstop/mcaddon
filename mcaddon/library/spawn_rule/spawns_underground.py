__all__ = ["SpawnRuleSpawnsUnderground"]


from .component import SpawnRuleComponent
from typing import ClassVar


@SpawnRuleComponent.register
class SpawnRuleSpawnsUnderground(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_underground)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:spawns_underground"
