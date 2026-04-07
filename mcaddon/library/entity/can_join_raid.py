__all__ = ["EntityCanJoinRaidComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityCanJoinRaidComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_can_join_raid)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:can_join_raid"
