__all__ = ["EntitySkinIdComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntitySkinIdComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_skin_id)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:skin_id"

    value: int = 0
