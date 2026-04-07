__all__ = ["EntityDragonLandingComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityDragonLandingComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_dragonlanding)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.dragonlanding"
