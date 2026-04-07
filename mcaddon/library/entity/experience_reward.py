__all__ = ["EntityExperienceRewardComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import Molang
from .component import EntityComponent


@EntityComponent.register
class EntityExperienceRewardComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_experience_reward)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:experience_reward"

    on_bred: Optional[Molang | int] = None
    on_death: Optional[Molang | int] = None
