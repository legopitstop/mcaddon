__all__ = ["EntityCanClimbComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityCanClimbComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_can_climb)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:can_climb"
