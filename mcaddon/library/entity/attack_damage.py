__all__ = ["EntityAttackDamageComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityAttackDamageComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_attack_damage)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:attack_damage"

    value: int
