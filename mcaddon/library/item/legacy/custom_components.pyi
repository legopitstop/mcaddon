from ..component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemCustomComponentsComponent"]

class ItemCustomComponentsComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_custom_components)

    This type is now deprecated, and no longer in use in the latest versions of Minecraft.
    """

    value: list[str] = ...

    def add(self, *component: str) -> "ItemCustomComponentsComponent": ...
