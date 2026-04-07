__all__ = ["EntityOcelotSitOnBlockComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityOcelotSitOnBlockComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_ocelot_sit_on_block)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.ocelot_sit_on_block"

    speed_multiplier: float = 1
