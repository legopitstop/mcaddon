__all__ = ["EntityGroupSizeComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field

from mcaddon.library.filter import Filter
from .component import EntityComponent


@EntityComponent.register
class EntityGroupSizeComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_group_size)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:group_size"

    filters: Optional[List[Filter] | Filter] = Field(default_factory=list)
    radius: float = 16
