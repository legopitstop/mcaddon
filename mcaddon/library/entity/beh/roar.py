__all__ = ["EntityRoarComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityRoarComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_roar)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.roar"

    duration: float = 0
