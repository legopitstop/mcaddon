__all__ = ["EntityBribeableComponent"]

from typing import List, ClassVar
from pydantic import Field
from .component import EntityComponent


@EntityComponent.register
class EntityBribeableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_bribeable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:bribeable"

    bribe_cooldown: float = 2
    bribe_items: List[str] = Field(default_factory=list)
