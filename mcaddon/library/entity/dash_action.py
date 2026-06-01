__all__ = ["EntityDashActionComponent"]

from typing import Optional, ClassVar
from mcaddon.library.constants import DashActionDirection
from .component import EntityComponent


@EntityComponent.register
class EntityDashActionComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_dash_action)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:dash_action"

    cooldown_time: float
    horizontal_momentum: float
    vertical_momentum: float
    can_dash_underwater: Optional[bool] = None
    direction: Optional[DashActionDirection] = None
