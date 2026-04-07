__all__ = ["EntityRendersWhenInvisibleComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityRendersWhenInvisibleComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_renders_when_invisible)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:renders_when_invisible"
