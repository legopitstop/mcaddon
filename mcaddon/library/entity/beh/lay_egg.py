__all__ = ["EntityLayEggComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field

from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityLayEggComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_lay_egg)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.lay_egg"

    allow_laying_from_below: bool = False
    egg_type: str = "minecraft:turtle_egg"
    goal_radius: float = 0.5
    lay_egg_sound: str = "lay_egg"
    lay_seconds: float = 10
    on_lay: Optional[EntityTriggerEvent] = None
    search_height: int = 1
    search_range: int = 0
    speed_multiplier: float = 1
    target_blocks: List[str] = Field(default=["minecraft:sand"])
    target_materials_above_block: List[str] = Field(default=["air"])
    use_default_animation: bool = True
