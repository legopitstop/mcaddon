__all__ = ["EntityWantsJockeyComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityWantsJockeyComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_wants_jockey)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:wants_jockey"
