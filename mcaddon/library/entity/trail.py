__all__ = ["EntityTrailComponent"]

from typing import Optional, ClassVar
from mcaddon.core.types import Vector3
from mcaddon.library.filter import Filter
from .component import EntityComponent


@EntityComponent.register
class EntityTrailComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trail)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:trail"

    block_type: str = "air"
    spawn_filter: Optional[Filter] = None
    spawn_offset: Vector3 = (0, 0, 0)
