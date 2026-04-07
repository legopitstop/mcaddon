__all__ = ["EntityAnnotationBreakDoorComponent"]

from mcaddon.library.constants import Difficulty
from typing import ClassVar
from mcaddon.library.entity.component import EntityComponent


@EntityComponent.register
class EntityAnnotationBreakDoorComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_annotation_break_door)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:annotation.break_door"

    break_time: int = 12
    min_difficulty: Difficulty = Difficulty.HARD
