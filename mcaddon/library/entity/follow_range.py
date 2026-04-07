__all__ = ["EntityFollowRangeComponent"]

from .component import EntityAttributeComponent, EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityFollowRangeComponent(EntityAttributeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_follow_range)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:follow_range"
