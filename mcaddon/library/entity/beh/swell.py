__all__ = ["EntitySwellComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntitySwellComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swell)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.swell"

    start_distance: float = 10
    stop_distance: float = 2
