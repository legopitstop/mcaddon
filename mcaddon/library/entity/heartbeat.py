__all__ = ["EntityHeartbeatComponent"]

from molang.dsl import MolangExpr
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityHeartbeatComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_heartbeat)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:heartbeat"

    interval: MolangExpr | float = 1
    sound_event: str = "heartbeat"
