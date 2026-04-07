__all__ = ["EntityLeashableToComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityLeashableToComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_leashable_to)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:leashable_to"

    can_retrieve_from: bool = False
