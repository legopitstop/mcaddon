__all__ = ["EntityCroakComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.filter import Filter
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityCroakComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_croak)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.croak"

    duration: Optional[NumberRange | float] = None
    filters: Optional[Filter] = None
    interval: Optional[NumberRange] = None
