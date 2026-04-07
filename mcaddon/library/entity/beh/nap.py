__all__ = ["EntityNapComponent"]

from typing import Optional, ClassVar
from mcaddon.library.filter import Filter
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityNapComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_nap)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.nap"

    can_nap_filters: Optional[Filter] = None
    cooldown_max: float = 0
    cooldown_min: float = 0
    mob_detect_dist: float = 6
    mob_detect_height: float = 6
    wake_mob_exceptions: Optional[Filter] = None
