__all__ = ["SpawnRuleSpawnsOnSurface"]


from .component import SpawnRuleComponent
from typing import ClassVar


@SpawnRuleComponent.register
class SpawnRuleSpawnsOnSurface(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_on_surface)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:spawns_on_surface"
