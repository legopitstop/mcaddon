__all__ = ["EntityInputAirControlledComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityInputAirControlledComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_input_air_controlled)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:input_air_controlled"

    backwards_movement_modifier: float = 0.5
    strafe_speed_modifier: float = 0.4
