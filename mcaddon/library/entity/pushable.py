__all__ = ["EntityPushableComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityPushableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_pushable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:pushable"

    is_pushable: bool = False
    is_pushable_by_piston: bool = False
