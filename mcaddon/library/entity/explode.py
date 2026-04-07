__all__ = ["EntityExplodeComponent", "ExplodeAdd"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel, NumberRange
from .component import EntityComponent


class ExplodeAdd(BaseModel):
    component_groups: List[str] = Field(default_factory=list)


@EntityComponent.register
class EntityExplodeComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_explode)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:explode"

    add: Optional[ExplodeAdd] = None
    allow_underwater: bool = False
    breaks_blocks: bool = True
    causes_fire: bool = False
    damage_scaling: int = 1
    destroy_affected_by_griefing: bool = False
    fire_affected_by_griefing: bool = False
    fuse_length: Optional[float | NumberRange] = None
    fuse_lit: bool = False
    knockback_scaling: float = 1
    max_resistance: float = 3.40282e38
    negates_fall_damage: bool = False
    particle_effect: str = "explosion"
    power: float = 3
    sound_effect: str = "explode"
    toggles_blocks: bool = False
