__all__ = ["ItemDurabilitySensorComponent"]

from typing import Optional, ClassVar
from .component import ItemComponent


@ItemComponent.register
class ItemDurabilitySensorComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_durability_sensor)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:durability_sensor"

    durability: int = 0
    particle_type: Optional[str] = None
    sound_event: Optional[str] = None
