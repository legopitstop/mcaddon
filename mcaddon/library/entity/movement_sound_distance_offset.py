__all__ = ["EntityMovementSoundDistanceOffsetComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityMovementSoundDistanceOffsetComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement_sound_distance_offset)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:movement_sound_distance_offset"

    value: float = 0
