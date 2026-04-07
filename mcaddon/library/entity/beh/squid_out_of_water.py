__all__ = ["EntitySquidOutOfWaterComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntitySquidOutOfWaterComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_squid_out_of_water)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.squid_out_of_water"
