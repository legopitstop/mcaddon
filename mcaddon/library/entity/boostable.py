__all__ = ["EntityBoostableComponent", "BoostItem"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from .component import EntityComponent


class BoostItem(BaseModel):
    item: str
    replace_item: str
    damage: int = 1


@EntityComponent.register
class EntityBoostableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_boostable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:boostable"

    boost_items: List[BoostItem] = Field(default_factory=list)
    duration: float = 3
    speed_multiplier: float = 1
