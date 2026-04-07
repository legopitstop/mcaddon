__all__ = ["EntitySnackingComponent"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntitySnackingComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_snacking)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.snacking"

    items: List[str] = Field(default_factory=list)
    snacking_cooldown: float = 7.5
    snacking_cooldown_min: float = 0.5
    snacking_stop_chance: float = 0.0017
