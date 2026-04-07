__all__ = ["EntityReceiveLoveComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityReceiveLoveComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_receive_love)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.receive_love"
