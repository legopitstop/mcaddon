__all__ = ["EntityRestrictSunComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityRestrictSunComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_restrict_sun)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.restrict_sun"
