__all__ = ["EntityDrinkPotionComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field, BaseModel
from mcaddon.library.filter import Filter
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


class Potion(BaseModel):
    id: int = -1
    chance: float = 1
    filters: Optional[Filter] = None


@EntityComponent.register
class EntityDrinkPotionComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_drink_potion)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.drink_potion"

    potions: List[Potion] = Field(default_factory=list)
    speed_modifier: float = 0
