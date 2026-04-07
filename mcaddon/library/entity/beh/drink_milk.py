__all__ = ["EntityDrinkMilkComponent"]

from typing import Optional, ClassVar
from mcaddon.library.filter import Filter
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityDrinkMilkComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_drink_milk)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.drink_milk"

    cooldown_seconds: float = 5
    filters: Optional[Filter] = None
