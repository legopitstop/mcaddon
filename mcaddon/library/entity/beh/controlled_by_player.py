__all__ = ["EntityControlledByPlayerComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityControlledByPlayerComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_controlled_by_player)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.controlled_by_player"

    fractional_rotation: float = 0.5
    fractional_rotation_limit: float = 5
    mount_speed_multiplier: float = 1
