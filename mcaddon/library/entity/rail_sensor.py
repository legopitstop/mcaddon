__all__ = ["EntityRailSensorComponent"]

from typing import Optional, ClassVar
from .event import EntityTriggerEvent
from .component import EntityComponent


@EntityComponent.register
class EntityRailSensorComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rail_sensor)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:rail_sensor"

    check_block_types: bool = False
    eject_on_activate: bool = True
    eject_on_deactivate: bool = False
    on_activate: Optional[EntityTriggerEvent] = None
    on_deactivate: Optional[EntityTriggerEvent] = None
    tick_command_block_on_activate: bool = True
    tick_command_block_on_deactivate: bool = False
