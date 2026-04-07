__all__ = ["EntitySquidDiveComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntitySquidDiveComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_squid_dive)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.squid_dive"
