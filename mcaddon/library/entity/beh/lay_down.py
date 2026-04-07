__all__ = ["EntityLayDownComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityLayDownComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_lay_down)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.lay_down"

    interval: int = 120
    random_stop_interval: int = 120
