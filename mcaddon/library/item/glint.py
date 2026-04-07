__all__ = [
    "ItemGlintComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemGlintComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_glint)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:glint"

    value: bool
