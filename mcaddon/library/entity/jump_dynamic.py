__all__ = ["EntityJumpDynamicComponent"]

from typing import ClassVar, Optional

from mcaddon.core.base import BaseModel

from .component import EntityComponent


class SkipData(BaseModel):
    animation_duration: int
    distance_scale: float
    height: float
    jump_delay: int


@EntityComponent.register
class EntityJumpDynamicComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_jump.dynamic)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:jump.dynamic"

    fast_skip_data: Optional[SkipData] = None
    regular_skip_data: Optional[SkipData] = None
