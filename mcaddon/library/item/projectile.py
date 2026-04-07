__all__ = [
    "ItemProjectileComponent",
]

from typing import ClassVar
from .component import ItemComponent


@ItemComponent.register
class ItemProjectileComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_projectile)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:projectile"

    projectile_entity: str
    minimum_critical_power: float = 0
