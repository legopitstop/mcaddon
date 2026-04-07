__all__ = ["EntityBurnsInDaylightComponent"]

from typing import Optional, ClassVar
from mcaddon.library.constants import EquipmentSlot
from mcaddon.core.base import ValueComponent
from .component import EntityComponent


@EntityComponent.register
class EntityBurnsInDaylightComponent(ValueComponent, EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_burns_in_daylight)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:burns_in_daylight"

    value: bool = True
    protection_slot: Optional[EquipmentSlot] = None
