__all__ = ["EntityHorseJumpStrengthComponent"]

from typing import Optional, List, ClassVar
from mcaddon.core.base import NumberRange
from .component import EntityComponent


@EntityComponent.register
class EntityHorseJumpStrengthComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_horse.jump_strength)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:horse.jump_strength"

    value: Optional[List[NumberRange] | NumberRange | float] = None
