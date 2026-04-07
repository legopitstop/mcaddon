from .component import ItemComponent
from mcaddon.core.base import NumberRange

__all__ = ["ItemPiercingWeaponComponent"]

class ItemPiercingWeaponComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_piercing_weapon)
    """

    hitbox_margin: float = ...
    reach: NumberRange = ...
    creative_reach: NumberRange = ...
