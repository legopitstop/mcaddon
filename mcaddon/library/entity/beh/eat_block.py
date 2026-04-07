__all__ = ["EntityEatBlockComponent"]

from typing import List, Optional, ClassVar
from molang.dsl import MolangExpr
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


class EatBlock(BaseModel):
    eat_block: str
    replace_block: Optional[str] = None


@EntityComponent.register
class EntityEatBlockComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_eat_block)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.eat_block"

    eat_and_replace_block_pairs: List[EatBlock] = Field(default_factory=list)
    on_eat: Optional[EntityTriggerEvent] = None
    success_chance: MolangExpr | float = 0.02
    time_until_eat: float = 1.8
