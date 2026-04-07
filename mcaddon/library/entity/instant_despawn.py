__all__ = ["EntityInstantDespawnComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityInstantDespawnComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_instant_despawn)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:instant_despawn"

    remove_child_entities: bool = False
