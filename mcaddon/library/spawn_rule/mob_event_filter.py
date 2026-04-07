__all__ = ["SpawnRuleMobEventFilter"]


from .component import SpawnRuleComponent
from typing import ClassVar


@SpawnRuleComponent.register
class SpawnRuleMobEventFilter(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/mob_event_filter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:mob_event_filter"

    event: str
