__all__ = ["EntityRideableComponent", "RideableSeat"]

from molang.dsl import MolangExpr
from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.library.constants import DismountMode
from mcaddon.core.base import BaseModel
from mcaddon.core.types import Vector3
from .event import EntityTriggerEvent
from .component import EntityComponent


class RideableSeat(BaseModel):
    camera_relax_distance_smoothing: Optional[float] = None
    lock_rider_rotation: float = 181
    max_rider_count: int = 0
    min_rider_count: int = 0
    position: Vector3 = (0, 0, 0)
    rotate_rider_by: MolangExpr | float = 0
    third_person_camera_radius: Optional[float] = 0


@EntityComponent.register
class EntityRideableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rideable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:rideable"

    controlling_seat: int = 0
    crouching_skip_interact: bool = True
    dismount_mode: DismountMode = DismountMode.DEFAULT
    family_types: List[str] = Field(default_factory=list)
    interact_text: Optional[str] = None
    on_rider_enter_event: Optional[EntityTriggerEvent | str] = None
    on_rider_exit_event: Optional[EntityTriggerEvent | str] = None
    passenger_max_width: float = 0
    priority: Optional[int] = None
    pull_in_entities: bool = False
    rider_can_interact: bool = False
    seat_count: int = 1
    seats: RideableSeat | List[RideableSeat] = Field(default_factory=list)
    pulls_in_entities: Optional[bool] = False
