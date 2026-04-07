__all__ = ["SpawnRuleSpawnsUnderwater"]


from .component import SpawnRuleComponent
from typing import ClassVar


@SpawnRuleComponent.register
class SpawnRuleSpawnsUnderwater(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_underwater)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:spawns_underwater"
