__all__ = ["EntityScaleComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityScaleComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_scale)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:scale"

    value: float = 1
