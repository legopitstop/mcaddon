__all__ = ["EntityCanFlyComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityCanFlyComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_can_fly)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:can_fly"
