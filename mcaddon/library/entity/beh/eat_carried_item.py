__all__ = ["EntityEatCarriedItemComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityEatCarriedItemComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_eat_carried_item)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.eat_carried_item"

    delay_before_eating: Optional[float] = None
