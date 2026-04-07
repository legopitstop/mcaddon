__all__ = ["EntityPushThroughComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityPushThroughComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_push_through)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:push_through"

    value: float = 0
