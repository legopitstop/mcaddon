__all__ = [
    "ItemDamageAbsorptionComponent",
]

from typing import List, ClassVar
from pydantic import Field
from .component import ItemComponent


@ItemComponent.register
class ItemDamageAbsorptionComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_durability_sensor)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:damage_absorption"

    absorbable_causes: List[str] = Field(default_factory=list)
