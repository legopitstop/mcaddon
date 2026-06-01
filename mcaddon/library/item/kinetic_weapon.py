__all__ = ["ItemKineticWeaponComponent", "ItemKineticEffectConditions"]

from typing import ClassVar
from mcaddon.core.base import NumberRange, NumberMinMax, BaseModel
from .component import ItemComponent


class ItemKineticEffectConditions(BaseModel):
    max_duration: int = -1
    min_relative_speed: float = 0
    min_speed: float = 0


@ItemComponent.register
class ItemKineticWeaponComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_kinetic_weapon)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:kinetic_weapon"

    damage_conditions: ItemKineticEffectConditions
    dismount_conditions: ItemKineticEffectConditions
    knockback_conditions: ItemKineticEffectConditions
    damage_modifier: float = 0
    damage_multiplier: float = 1
    delay: int = 0

    hitbox_margin: float = 0.25
    reach: NumberRange = NumberMinMax(min=2.0, max=4.5)
    creative_reach: NumberRange = NumberMinMax(min=2.0, max=7.5)
