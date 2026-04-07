__all__ = ["EntityCelebrateHuntComponent"]

from typing import Optional, ClassVar
from mcaddon.library.filter import Filter, FilterTest
from mcaddon.core.base import NumberRange
from .component import EntityComponent


@EntityComponent.register
class EntityCelebrateHuntComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_celebrate_hunt)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:celebrate_hunt"

    celebrate_sound: str
    broadcast: bool = True
    celeberation_targets: Optional[FilterTest] = None
    celebration_targets: Optional[Filter] = None
    duration: int = 4
    radius: float = 16
    sound_interval: int | NumberRange = 0
