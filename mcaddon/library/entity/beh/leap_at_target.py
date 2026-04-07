__all__ = ["EntityLeapAtTargetComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityLeapAtTargetComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_leap_at_target)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.leap_at_target"

    must_be_on_ground: bool = True
    set_persistent: Optional[int] = None
    target_dist: float = False
    yd: float = 0
