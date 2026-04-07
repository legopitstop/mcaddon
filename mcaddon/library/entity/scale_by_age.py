__all__ = ["EntityScaleByAgeComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityScaleByAgeComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_scale_by_age)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:scale_by_age"

    end_scale: float = 1
    start_scale: float = 1
