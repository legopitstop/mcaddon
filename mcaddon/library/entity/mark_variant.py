__all__ = ["EntityMarkVariantComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityMarkVariantComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_mark_variant)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:mark_variant"

    value: int = 0
