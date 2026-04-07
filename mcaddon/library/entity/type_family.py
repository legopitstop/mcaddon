__all__ = ["EntityTypeFamilyComponent"]

from typing import List, ClassVar
from pydantic import Field
from .component import EntityComponent


@EntityComponent.register
class EntityTypeFamilyComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_type_family)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:type_family"

    family: List[str] = Field(default_factory=list)
