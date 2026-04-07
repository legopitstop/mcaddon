__all__ = ["EntityPlayerRideTamedComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityPlayerRideTamedComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_player_ride_tamed)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.player_ride_tamed"
