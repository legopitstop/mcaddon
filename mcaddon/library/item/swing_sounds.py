__all__ = [
    "ItemSwingSoundsComponent",
]

from typing import ClassVar
from typing import Optional
from .component import ItemComponent


@ItemComponent.register
class ItemSwingSoundsComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_swing_sounds)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:swing_sounds"

    attack_critical_hit: Optional[str] = None
    attack_hit: Optional[str] = None
    attack_miss: Optional[str] = None
