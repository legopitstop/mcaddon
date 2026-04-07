__all__ = ["EntityRiseToLiquidLevelComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityRiseToLiquidLevelComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_rise_to_liquid_level)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.rise_to_liquid_level"

    liquid_y_offset: float = 0
    rise_delta: float = 0
    sink_delta: float = 0
