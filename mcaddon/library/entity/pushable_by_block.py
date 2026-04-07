__all__ = ["EntityPushableByBlockComponent"]

from typing import ClassVar

from .component import EntityComponent


@EntityComponent.register
class EntityPushableByBlockComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_pushable_by_block)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:pushable_by_block"
