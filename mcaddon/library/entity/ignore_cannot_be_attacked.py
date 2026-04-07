__all__ = ["EntityIgnoreCannotBeAttackedComponent"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.library.filter import Filter
from .component import EntityComponent


@EntityComponent.register
class EntityIgnoreCannotBeAttackedComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ignore_cannot_be_attacked)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:ignore_cannot_be_attacked"

    filters: List[Filter] | Filter = Field(default_factory=list)
