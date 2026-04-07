__all__ = ["EntityDamageOverTimeComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityDamageOverTimeComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_damage_over_time)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:damage_over_time"

    damage_per_hurt: int = 1
    time_between_hurt: float = 0
