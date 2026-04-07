__all__ = ["EntitySlimeFloatComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntitySlimeFloatComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_slime_float)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.slime_float"

    jump_chance_percentage: float = 0.8
    speed_multiplier: float = 1.2
