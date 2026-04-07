__all__ = ["EntityJumpStaticComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityJumpStaticComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_jump.static)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:jump.static"

    jump_power: float = 0.42
