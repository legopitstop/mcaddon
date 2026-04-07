__all__ = ["EntitySneezeComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
    EntityType,
)


@EntityComponent.register
class EntitySneezeComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_sneeze)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.sneeze"

    cooldown_time: float = 0
    drop_item_chance: float = 1
    entity_types: List[EntityType] = Field(default_factory=list)
    loot_table: Optional[str] = None
    prepare_sound: Optional[str] = None
    prepare_time: float = 1
    probability: float = 0.02
    sound: Optional[str] = None
    within_radius: float = 0
