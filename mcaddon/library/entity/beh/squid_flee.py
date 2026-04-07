__all__ = ["EntitySquidFleeComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntitySquidFleeComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_squid_flee)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.squid_flee"
