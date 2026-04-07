__all__ = ["EntitySwimIdleComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntitySwimIdleComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swim_idle)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.swim_idle"
    idle_time: float = 5
    success_rate: float = 0.1
