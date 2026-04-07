__all__ = ["EntityMoveToPoiComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityMoveToPoiComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_poi)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.move_to_poi"

    poi_type: Optional[str] = None
    speed_multiplier: float = 1
