__all__ = ["EntityFlyingSpeedComponent"]

from .component import EntityAttributeComponent, EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityFlyingSpeedComponent(EntityAttributeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_flying_speed)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:flying_speed"
