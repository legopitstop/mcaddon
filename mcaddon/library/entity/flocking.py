__all__ = ["EntityFlockingComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityFlockingComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_flocking)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:flocking"

    block_distance: float = 0
    block_weight: float = 0
    breach_influence: float = 0
    cohesion_threshold: float = 1
    cohesion_weight: float = 1
    goal_weight: float = 0
    high_flock_limit: float = 0
    in_water: bool = False
    influence_radius: float = 0
    innner_cohesion_threshold: float = 0
    loner_chance: float = 0
    low_flock_limit: float = 0
    match_variants: bool = False
    max_height: float = 0
    min_height: float = 0
    separation_threshold: float = 2
    separation_weight: float = 1
    use_center_of_mass: bool = False
