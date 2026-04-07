__all__ = ["EntityBalloonableComponent"]

from typing import Optional, ClassVar
from .component import EntityComponent
from .event import EntityTriggerEvent


@EntityComponent.register
class EntityBalloonableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_balloonable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:balloonable"

    mass: float = 1
    max_distance: int = 10
    soft_distance: float = 2
    on_balloon: Optional[EntityTriggerEvent] = None
    on_unballoon: Optional[EntityTriggerEvent] = None
