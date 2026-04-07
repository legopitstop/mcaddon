__all__ = ["EntityBreathableComponent"]

from typing import List, Optional, ClassVar

from pydantic import Field
from .component import EntityComponent


@EntityComponent.register
class EntityBreathableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_breathable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:breathable"

    breathe_blocks: List[str] = Field(default_factory=list)
    non_breathe_blocks: List[str] = Field(default_factory=list)
    breathes_air: bool = True
    breathes_lava: bool = True
    breathes_solids: bool = False
    breathes_water: bool = False
    generates_bubbles: bool = True
    can_dehydrate: bool = False
    inhale_time: float = 0
    suffocate_time: float = -20
    suffocateTime: float = -1
    total_supply: int = 15
    totalSupply: Optional[float] = None
