__all__ = ["EntityCombatRegenerationComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityCombatRegenerationComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_combat_regeneration)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:combat_regeneration"

    apply_to_family: bool = False
    apply_to_self: bool = False
    regeneration_duration: int = 5
