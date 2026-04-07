__all__ = ["EntityTeleportToOwnerComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
)
from mcaddon.library.filter import Filter


@EntityComponent.register
class EntityTeleportToOwnerComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_teleport_to_owner)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.teleport_to_owner"

    cooldown: float = 1
    filters: Optional[Filter] = None
