__all__ = ["EntityBarterComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityBarterComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_barter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:barter"

    barter_table: str
    cooldown_after_being_attacked: int = 0
