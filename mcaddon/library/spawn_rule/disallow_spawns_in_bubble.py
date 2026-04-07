__all__ = ["SpawnRuleDisallowSpawnsInBubble"]


from .component import SpawnRuleComponent
from typing import ClassVar


@SpawnRuleComponent.register
class SpawnRuleDisallowSpawnsInBubble(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/disallow_spawns_in_bubble)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:disallow_spawns_in_bubble"
