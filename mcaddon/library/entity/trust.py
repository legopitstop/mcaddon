__all__ = ["EntityTrustComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityTrustComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trust)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:trust"
