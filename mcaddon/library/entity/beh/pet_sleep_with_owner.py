__all__ = ["EntityPetSleepWithOwnerComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityPetSleepWithOwnerComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_pet_sleep_with_owner)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.pet_sleep_with_owner"

    goal_radius: float = 0.5
    search_height: int = 1
    search_radius: Optional[float] = None
    search_range: int = 0
    speed_multiplier: float = 1
