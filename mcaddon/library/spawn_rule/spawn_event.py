__all__ = ["SpawnRuleSpawnEvent"]


from .component import SpawnRuleComponent
from typing import ClassVar


@SpawnRuleComponent.register
class SpawnRuleSpawnEvent(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawn_event)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:spawn_event"

    event: str
