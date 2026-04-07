__all__ = ["EntityBuoyantComponent"]

from typing import List, ClassVar, Optional
from pydantic import Field
from .component import EntityComponent


@EntityComponent.register
class EntityBuoyantComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_bouyant)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:buoyant"

    movement_type: Optional[str] = None
    can_auto_step_from_liquid: bool = True
    apply_gravity: bool = True
    base_buoyancy: float = 1
    big_wave_probability: float = 0.03
    big_wave_speed: float = 10
    drag_down_on_buoyancy_removed: float = 0
    liquid_blocks: List[str] = Field(default_factory=list)
    simulate_waves: bool = True
