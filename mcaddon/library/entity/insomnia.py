__all__ = ["EntityInsomniaComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityInsomniaComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_insomnia)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:insomnia"

    days_until_insomnia: float = 3
