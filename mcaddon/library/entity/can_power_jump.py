__all__ = ["EntityCanPowerJumpComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityCanPowerJumpComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_can_power_jump)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:can_power_jump"
