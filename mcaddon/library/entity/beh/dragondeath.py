__all__ = ["EntityDragonDeathComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityDragonDeathComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_dragondeath)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.dragondeath"
