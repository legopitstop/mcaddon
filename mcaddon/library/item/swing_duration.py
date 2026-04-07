__all__ = [
    "ItemSwingDurationComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemSwingDurationComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_swing_duration)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:swing_duration"

    value: float = 0.30000001192092896
