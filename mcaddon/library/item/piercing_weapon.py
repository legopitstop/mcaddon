__all__ = [
    "ItemPiercingWeaponComponent",
]

from typing import ClassVar
from mcaddon.core.base import NumberRange, NumberMinMax
from .component import ItemComponent


@ItemComponent.register
class ItemPiercingWeaponComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_piercing_weapon)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:piercing_weapon"

    hitbox_margin: float = 0.25
    reach: NumberRange = NumberMinMax(min=2.0, max=4.5)
    creative_reach: NumberRange = NumberMinMax(min=2.0, max=7.5)
