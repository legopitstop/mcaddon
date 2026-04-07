__all__ = ["EntityAttackComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from .component import EntityComponent


@EntityComponent.register
class EntityAttackComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_attack)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:attack"
    damage: Optional[NumberRange | float] = None
    effect_duration: float = 0
    effect_name: Optional[str] = None
