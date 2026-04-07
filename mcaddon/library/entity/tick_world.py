__all__ = ["EntityTickWorldComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityTickWorldComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_tick_world)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:tick_world"

    distance_to_players: float = 128
    never_despawn: bool = True
    radius: int = 2
