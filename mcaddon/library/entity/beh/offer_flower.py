__all__ = ["EntityOfferFlowerComponent"]

from typing import Optional, ClassVar
from mcaddon.library.filter import Filter
from mcaddon.core.types import Vector3
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityOfferFlowerComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_offer_flower)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.offer_flower"

    chance_to_start: float = 0
    filters: Optional[Filter] = None
    max_head_rotation_y: float = 30
    max_offer_flower_duration: float = 20
    max_rotation_x: float = 30
    search_area: Vector3 = (6, 2, 6)
