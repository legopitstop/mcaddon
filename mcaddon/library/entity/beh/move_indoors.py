__all__ = ["EntityMoveIndoorsComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityMoveIndoorsComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_indoors)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.move_indoors"

    speed_multiplier: float = 0.8
    timeout_cooldown: float = 8
