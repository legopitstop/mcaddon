__all__ = ["EntityAnnotationOpenDoorComponent"]

from mcaddon.library.entity.component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityAnnotationOpenDoorComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_annotation_open_door)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:annotation.open_door"
