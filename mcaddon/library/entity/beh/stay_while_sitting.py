__all__ = ["EntityStayWhileSittingComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityStayWhileSittingComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stay_while_sitting)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.stay_while_sitting"
