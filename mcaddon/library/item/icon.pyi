from typing import Optional
from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemIconComponent"]

class ItemIconComponent(ItemComponent, ValueComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_icon)
    """

    textures: dict[str, str] = ...
    texture: str | None = ...

    def add(self, texture: str, key: Optional[str] = None) -> "ItemIconComponent": ...
