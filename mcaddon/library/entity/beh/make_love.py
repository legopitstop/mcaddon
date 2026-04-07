__all__ = ["EntityMakeLoveComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityMakeLoveComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_make_love)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.make_love"
