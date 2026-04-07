__all__ = ["ItemFoodComponent", "FoodEffect"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel, ItemLike
from mcaddon.core.types import Vector3
from mcaddon.library.constants import SaturationModifierType
from .component import ItemComponent


class FoodEffect(BaseModel):
    name: str
    amplifier: float
    duration: float
    chance: float = 1.0


@ItemComponent.register
class ItemFoodComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_food)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:food"

    nutrition: int = 0
    saturation_modifier: float | SaturationModifierType = 0.6000000238418579
    can_always_eat: bool = False
    cooldown_time: Optional[float] = None
    cooldown_type: Optional[str] = None
    effects: List[FoodEffect] = Field(default_factory=list)
    is_meat: Optional[bool] = None
    remove_effects: List[str] = Field(default_factory=list)
    using_converts_to: Optional[ItemLike] = None

    on_use_action: Optional[str] = Field(deprecated=True, default=None)
    on_use_range: Optional[Vector3] = Field(deprecated=True, default=None)
