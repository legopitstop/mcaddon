__all__ = ["EntityInvestigateSuspiciousLocationComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityInvestigateSuspiciousLocationComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_investigate_suspicious_location)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.investigate_suspicious_location"

    goal_radius: float = 1.5
    speed_multiplier: float = 1
