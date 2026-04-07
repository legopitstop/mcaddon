__all__ = ["EntityBehaviorBarterComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityBehaviorBarterComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_barter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.barter"
