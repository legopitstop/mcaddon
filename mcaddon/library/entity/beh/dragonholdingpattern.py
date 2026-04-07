__all__ = ["EntityDragonHoldingPatternComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityDragonHoldingPatternComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_dragonholdingpattern)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.dragonholdingpattern"
