__all__ = ["EntityKnockbackResistanceComponent"]

from .component import EntityComponent, EntityAttributeComponent
from typing import ClassVar


@EntityComponent.register
class EntityKnockbackResistanceComponent(EntityAttributeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_knockback_resistance)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:knockback_resistance"
