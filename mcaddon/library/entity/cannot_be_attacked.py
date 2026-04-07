__all__ = ["EntityCannotBeAttackedComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityCannotBeAttackedComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_cannot_be_attacked)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:cannot_be_attacked"
