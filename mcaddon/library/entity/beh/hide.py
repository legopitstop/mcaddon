__all__ = ["EntityBehaviorHideComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityBehaviorHideComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_hide)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.hide"

    duration: float = 1
    poi_type: Optional[str] = None
    speed_multiplier: float = 1
    timeout_cooldown: float = 8
