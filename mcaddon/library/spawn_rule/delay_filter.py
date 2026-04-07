__all__ = ["SpawnRuleDelayFilter"]


from .component import SpawnRuleComponent
from typing import ClassVar


@SpawnRuleComponent.register
class SpawnRuleDelayFilter(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/delay_filter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:delay_filter"

    max: int = 0
    min: int = 0
    identifier: str = ""
    spawn_chance: int = 100
