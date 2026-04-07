__all__ = ["EntityGameEventMovementTrackingComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityGameEventMovementTrackingComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_game_event_movement_tracking)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:game_event_movement_tracking"

    emit_flap: bool = False
    emit_move: bool = False
    emit_swim: bool = False
