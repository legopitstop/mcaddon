__all__ = ["EntityVariantComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityVariantComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_variant)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:variant"

    value: int = 0
