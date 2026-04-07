__all__ = ["EntityInputGroundControlledComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityInputGroundControlledComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_input_ground_controlled)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:input_ground_controlled"
