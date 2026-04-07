__all__ = ["EntityWalkAnimationSpeedComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityWalkAnimationSpeedComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_walk_animation_speed)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:walk_animation_speed"

    value: float = 1
