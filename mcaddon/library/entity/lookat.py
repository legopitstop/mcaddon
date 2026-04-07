__all__ = ["EntityLookAtComponent"]

from typing import ClassVar

from mcaddon.library.filter import Filter
from .component import EntityComponent


@EntityComponent.register
class EntityLookAtComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_lookat)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:lookat"

    search_radius: int
    set_target: bool
    look_cooldown: int
    filters: Filter
