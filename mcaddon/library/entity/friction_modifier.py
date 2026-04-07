__all__ = ["EntityFrictionModifierComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityFrictionModifierComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_friction_modifier)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:friction_modifier"

    value: float = 1
