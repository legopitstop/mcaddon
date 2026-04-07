__all__ = ["EntityPhysicsComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityPhysicsComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_physics)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:physics"

    has_collision: bool = False
    has_gravity: bool = False
    push_towards_closest_space: bool = False
