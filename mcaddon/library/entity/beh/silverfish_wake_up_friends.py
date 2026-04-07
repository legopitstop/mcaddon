__all__ = ["EntitySilverfishWakeUpFriendsComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntitySilverfishWakeUpFriendsComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_silverfish_wake_up_friends)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.silverfish_wake_up_friends"
