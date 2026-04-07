__all__ = ["EntityChargeHeldItemComponent"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityChargeHeldItemComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_charge_held_item)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.charge_held_item"

    items: List[str] = Field(default_factory=list)
