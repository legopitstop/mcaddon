__all__ = [
    "ItemCustomComponentsComponent",
]

from typing import List, ClassVar
from pydantic import Field

from mcaddon.core.base import ValueComponent
from ..component import ItemComponent
from deprecated import deprecated


@deprecated("This component is deprecated, register your own component instead.")
@ItemComponent.register
class ItemCustomComponentsComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_custom_components)

    This type is now deprecated, and no longer in use in the latest versions of Minecraft.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:custom_components"

    value: List[str] = Field(default_factory=list)

    def add(self, *component: str) -> "ItemCustomComponentsComponent":
        self.value.extend(component)
        return self
