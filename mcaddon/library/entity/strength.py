__all__ = ["EntityStrengthComponent"]

from .component import EntityComponent, EntityAttributeComponent
from typing import ClassVar


@EntityComponent.register
class EntityStrengthComponent(EntityAttributeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_strength)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:strength"
