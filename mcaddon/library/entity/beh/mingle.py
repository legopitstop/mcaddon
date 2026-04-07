__all__ = ["EntityMingleComponent"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityMingleComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_mingle)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.mingle"

    cooldown_time: float = 0
    duration: float = 1
    mingle_distance: float = 2
    mingle_partner_type: List[str] | str = Field(default_factory=list)
    speed_multiplier: float = 1
