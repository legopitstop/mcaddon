__all__ = ["EntityExhaustionValuesComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityExhaustionValuesComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_exhaustion_values)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:exhaustion_values"

    attack: float = 0.1
    damage: float = 0.1
    heal: float = 6
    jump: float = 0.05
    mine: float = 0.005
    sprint: float = 0.01
    sprint_jump: float = 0.2
    swim: float = 0.01
    walk: float = 0
    lunge: float = 0
