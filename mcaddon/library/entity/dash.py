__all__ = ["EntityDashComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityDashComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_dash)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:dash"

    cooldown_time: float = 1
    horizontal_momentum: float = 1
    vertical_momentum: float = 1
