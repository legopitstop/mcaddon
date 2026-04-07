__all__ = ["EntityManagedWanderingTraderComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityManagedWanderingTraderComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_managed_wandering_trader)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:managed_wandering_trader"
