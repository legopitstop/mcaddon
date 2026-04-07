__all__ = ["EntityLookedAtComponent", "LookAtLocation"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.library.filter import Filter
from mcaddon.core.base import BaseModel, NumberRange
from mcaddon.library.constants import SetTargetType, LineOfSightObstructionType
from .event import EntityTriggerEvent
from .component import EntityComponent


class LookAtLocation(BaseModel):
    location: str
    vertical_offset: float = 0


@EntityComponent.register
class EntityLookedAtComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_looked_at)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:looked_at"

    field_of_view: float = 26
    filters: Optional[Filter] = None
    find_players_only: bool = False
    line_of_sight_obstruction_type: LineOfSightObstructionType = (
        LineOfSightObstructionType.COLLISION
    )
    look_at_locations: List[LookAtLocation] = Field(default_factory=list)
    looked_at_cooldown: Optional[NumberRange | float] = None
    looked_at_event: Optional[EntityTriggerEvent] = None
    min_looked_at_duration: float = 0
    not_looked_at_event: Optional[EntityTriggerEvent] = None
    scale_fov_by_distance: bool = True
    search_radius: float = 10
    set_target: bool | SetTargetType = False
