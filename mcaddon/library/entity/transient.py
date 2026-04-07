__all__ = ["EntityTransientComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityTransientComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_transient)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:transient"
