__all__ = ["EntityRollComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityRollComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_roll)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.roll"

    probability: Optional[float] = None
