__all__ = ["EntityTransformationComponent", "EntityTransformationDelay"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from .event import EntityAddComponent
from .component import EntityComponent


class EntityTransformationDelay(BaseModel):
    block_assist_chance: float = 0
    block_chance: float = 0
    block_max: int = 0
    block_radius: int = 0
    block_types: List[str] = Field(default_factory=list)
    range_max: float = 0
    range_min: float = 0
    value: float = 0


@EntityComponent.register
class EntityTransformationComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_transformation)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:transformation"

    add: List[EntityAddComponent] = Field(default_factory=list)
    begin_transform_sound: Optional[str] = None
    delay: List[EntityTransformationDelay] | EntityTransformationDelay | float = Field(
        default_factory=list
    )
    drop_equipment: bool = False
    drop_inventory: bool = False
    into: Optional[str] = None
    keep_level: bool = False
    keep_owner: bool = False
    preserve_equipment: bool = False
    transformation_sound: Optional[str] = None
