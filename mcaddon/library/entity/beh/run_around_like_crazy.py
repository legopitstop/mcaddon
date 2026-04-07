__all__ = ["EntityRunAroundLikeCrazyComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityRunAroundLikeCrazyComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_run_around_like_crazy)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.run_around_like_crazy"

    speed_multiplier: float = 1
