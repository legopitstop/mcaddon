__all__ = ["EntityReflectProjectilesComponent"]

from typing import List, ClassVar
from molang.dsl import MolangExpr
from pydantic import Field
from .component import EntityComponent


@EntityComponent.register
class EntityReflectProjectilesComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_reflect_projectiles)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:reflect_projectiles"

    azimuth_angle: MolangExpr | float = 0
    elevation_angle: MolangExpr | float = 0
    reflected_projectiles: List[str] = Field(default_factory=list)
    reflection_scale: MolangExpr | float = 1
    reflection_sound: str = "reflect"
