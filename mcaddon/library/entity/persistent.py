__all__ = ["EntityPersistentComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityPersistentComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_persistent)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:persistent"
