__all__ = ["EntityAdmireItemComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityAdmireItemComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_admire_item)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:admire_item"

    cooldown_after_being_attacked: int = 0
    duration: int = 10
