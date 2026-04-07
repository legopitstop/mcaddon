__all__ = ["EntityEndermanTakeBlockComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityEndermanTakeBlockComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_enderman_take_block)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.enderman_take_block"
