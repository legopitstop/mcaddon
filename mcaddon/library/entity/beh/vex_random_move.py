__all__ = ["EntityVexRandomMoveComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityVexRandomMoveComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_vex_random_move)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.vex_random_move"
