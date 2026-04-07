__all__ = ["EntityBlockClimberComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityBlockClimberComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_block_climber)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:block_climber"
