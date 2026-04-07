__all__ = ["EntityDragonFlamingComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityDragonFlamingComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_dragonflaming)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.dragonflaming"

    cooldown_time: float = 10
    flame_time: float = 0.5
    ground_flame_count: int = 4
    roar_time: float = 2
