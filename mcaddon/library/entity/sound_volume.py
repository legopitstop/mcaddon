__all__ = ["EntitySoundVolumeComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntitySoundVolumeComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_sound_volume)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:sound_volume"

    value: float = 1
