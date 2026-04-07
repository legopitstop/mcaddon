__all__ = ["EntityMoveToLiquidComponent"]

from pydantic import field_validator
from typing import ClassVar
from mcaddon.library.constants import LiquidMaterialType
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityMoveToLiquidComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_liquid)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.move_to_liquid"

    goal_radius: float = 0.5
    material_type: LiquidMaterialType = LiquidMaterialType.ANY
    search_count: int = 10
    search_height: int = 1
    search_range: int = 0
    speed_multiplier: float = 1

    @field_validator("material_type", mode="before")
    @classmethod
    def coerce_enum(cls, v):
        return LiquidMaterialType.parse(v.lower())
