__all__ = ["EntitySwimUpForBreathComponent"]

from mcaddon.library.constants import LiquidMaterialType
from typing import ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntitySwimUpForBreathComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swim_up_for_breath)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.swim_up_for_breath"

    material_type: LiquidMaterialType = LiquidMaterialType.WATER
    search_height: int = 16
    search_radius: int = 4
    speed_mod: float = 1.4
