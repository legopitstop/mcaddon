__all__ = ["EntityCustomHitTestComponent"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.core.types import Vector3
from .component import EntityComponent


class Hitbox(BaseModel):
    width: float
    height: float
    pivot: Vector3


@EntityComponent.register
class EntityCustomHitTestComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_custom_hit_test)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:custom_hit_test"

    hitboxes: List[Hitbox] = Field(default_factory=list)
