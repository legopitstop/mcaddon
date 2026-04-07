__all__ = ["EntitySpawnEggInteractionComponent"]

from typing import ClassVar

from .component import EntityComponent


@EntityComponent.register
class EntitySpawnEggInteractionComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_spawn_egg_interaction)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:spawn_egg_interaction"
