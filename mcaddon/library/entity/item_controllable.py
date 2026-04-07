__all__ = ["EntityItemControllableComponent"]

from typing import List, ClassVar
from pydantic import Field
from .component import EntityComponent


@EntityComponent.register
class EntityItemControllableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_item_controllable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:item_controllable"

    control_items: List[str] | str = Field(default_factory=list)
