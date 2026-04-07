__all__ = ["EntityAngerLevelComponent"]

from typing import List, Optional, ClassVar

from molang.dsl import MolangExpr
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.library.filter import Filter
from .component import EntityComponent


class IncreaseSound(BaseModel):
    condition: MolangExpr
    sound: str


@EntityComponent.register
class EntityAngerLevelComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_anger_level)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:anger_level"

    anger_decrement_interval: int = 1
    angry_boost: int = 20
    angry_threshold: int = 80
    broadcast_anger: bool = False
    broadcast_anger_on_attack: bool = False
    broadcast_filters: Optional[Filter] = None
    broadcast_range: int = 20
    broadcast_targets: List[str] = Field(default_factory=list)
    calm_event: Optional[str] = None
    default_annoyingness: int = 0
    default_projectile_annoyingness: float
    duration: Optional[int] = None
    duration_delta: Optional[int] = None
    filters: Optional[Filter] = None
    max_anger: int = 100
    nuisance_filter: Filter
    on_increase_sounds: List[IncreaseSound] = Field(default_factory=list)
    remove_targets_below_angry_threshold: bool = True
    sound_interval: Optional[str] = None
