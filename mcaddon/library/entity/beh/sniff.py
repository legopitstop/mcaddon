__all__ = ["EntitySniffComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntitySniffComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_sniff)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.sniff"

    cooldown_range: Optional[NumberRange] = None
    duration: float = 1
    sniffing_radius: float = 5
    suspicion_radius_horizontal: float = 3
    suspicion_radius_vertical: float = 3
