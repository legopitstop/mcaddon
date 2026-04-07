__all__ = ["SpawnRuleBrightnessFilter"]


from .component import SpawnRuleComponent
from typing import ClassVar


@SpawnRuleComponent.register
class SpawnRuleBrightnessFilter(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/brightness_filter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:brightness_filter"

    adjust_for_weather: bool = False
    max: float = 15.0
    min: float = 0.0
