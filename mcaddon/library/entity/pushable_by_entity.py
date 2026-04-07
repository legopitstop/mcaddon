__all__ = ["EntityPushableByEntityComponent"]

from typing import ClassVar

from .component import EntityComponent


@EntityComponent.register
class EntityPushableByEntityComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_pushable_by_entity)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:pushable_by_entity"
