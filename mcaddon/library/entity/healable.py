__all__ = ["EntityHealableComponent", "HealableItem", "HealableEffect"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.library.filter import Filter
from mcaddon.core.base import BaseModel, ItemResult
from .component import EntityComponent


class HealableEffect(BaseModel):
    name: str
    chance: Optional[float] = None
    duration: Optional[int] = None
    amplifier: Optional[int] = None


class HealableItem(ItemResult):
    heal_amount: int = 1
    effects: List[HealableEffect] = Field(default_factory=list)


@EntityComponent.register
class EntityHealableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_healable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:healable"

    filters: Optional[Filter] = None
    force_use: bool = False
    items: List[HealableItem] = Field(default_factory=list)
