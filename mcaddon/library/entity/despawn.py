__all__ = ["EntityDespawnComponent", "DespawnFromDistance"]

from typing import List, Optional, ClassVar

from mcaddon.core.base import BaseModel
from mcaddon.library.filter import Filter
from .component import EntityComponent


class DespawnFromDistance(BaseModel):
    min_distance: int = 32
    max_distance: int = 128


@EntityComponent.register
class EntityDespawnComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_despawn)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:despawn"

    despawn_from_chance: bool = True
    despawn_from_distance: Optional[
        List[DespawnFromDistance] | int | DespawnFromDistance
    ] = None
    despawn_from_inactivity: bool = True
    despawn_from_simulation_edge: bool = True
    filters: Optional[Filter] = None
    min_range_inactivity_timer: int = 30
    min_range_random_chance: int = 800
    remove_child_entities: bool = False
