__all__ = ["EntityTeleportComponent"]

from mcaddon.core.types import Vector3
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityTeleportComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_teleport)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:teleport"

    dark_teleport_chance: float = 0.01
    light_teleport_chance: float = 0.01
    max_random_teleport_time: float = 20
    min_random_teleport_time: float = 0
    random_teleport_cube: Vector3 = (32, 16, 32)
    random_teleports: bool = True
    target_distance: float = 16
    target_teleport_chance: float = 1
