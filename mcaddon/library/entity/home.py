__all__ = ["EntityHomeComponent"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.library.constants import HomeRestrictionType
from .component import EntityComponent


@EntityComponent.register
class EntityHomeComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_home)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:home"

    home_block_list: List[str] = Field(default_factory=list)
    restriction_radius: int = 0
    restriction_type: HomeRestrictionType = HomeRestrictionType.NONE
