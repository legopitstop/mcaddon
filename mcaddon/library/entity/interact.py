__all__ = [
    "EntityInteractComponent",
    "ParticleOnStart",
    "SpawnItems",
    "RepairEntityItem",
]

from typing import List, Optional, ClassVar
from pydantic import Field, BaseModel

from mcaddon.library.constants import EquipmentSlot
from .component import EntityComponent
from .event import EntityTriggerEvent


class ParticleOnStart(BaseModel):
    particle_offset_towards_interactor: bool = False
    particle_type: Optional[str] = None
    particle_y_offset: float = 0
    copper_event: Optional[str] = None


class SpawnItems(BaseModel):
    table: str
    y_offset: float = 0


class RepairEntityItem(BaseModel):
    amount: int
    slot: EquipmentSlot


class Interaction(BaseModel):
    cooldown: Optional[float] = None
    give_item: Optional[bool | str] = None
    hurt_item: Optional[int] = None
    interact_text: Optional[str] = None
    on_interact: Optional[EntityTriggerEvent] = None
    play_sounds: Optional[str] = None
    swing: bool | str = False
    take_item: Optional[bool | str] = None
    transform_to_item: Optional[str] = None
    use_item: Optional[bool | str] = None
    vibration: Optional[str] = None
    particle_on_start: List[ParticleOnStart] | ParticleOnStart = Field(
        default_factory=list
    )
    repair_entity_item: List[RepairEntityItem] | RepairEntityItem = Field(
        default_factory=list
    )
    spawn_entities: List[str] | str = Field(default_factory=list)
    spawn_items: List[SpawnItems] | SpawnItems = Field(default_factory=list)


@EntityComponent.register
class EntityInteractComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_interact)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:interact"

    cooldown: float = 0
    cooldown_after_being_attacked: float = 0
    drop_item_slot: Optional[EquipmentSlot] = None
    drop_item_y_offset: float = 0
    equip_item_slot: Optional[EquipmentSlot] = None
    health_amount: int = 0
    hurt_item: int = 0
    interact_text: Optional[str] = None
    interactions: List[Interaction] | Interaction = Field(default_factory=list)
