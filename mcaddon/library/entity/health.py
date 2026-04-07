__all__ = ["EntityHealthComponent"]

from .component import EntityAttributeComponent, EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityHealthComponent(EntityAttributeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_health)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:health"
