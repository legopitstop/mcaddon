__all__ = ["EntityBodyRotationAlwaysFollowsHeadComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityBodyRotationAlwaysFollowsHeadComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_body_rotation_always_follows_head)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:body_rotation_always_follows_head"
