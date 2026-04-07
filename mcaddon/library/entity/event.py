__all__ = [
    "EntityEvent",
    "SequenceEvent",
    "RandomizeEvent",
    "EntityRemoveComponent",
    "EntityAddComponent",
    "EmitVibration",
    "PlaySoundEvent",
    "EmitParticleEvent",
    "EntityTriggerEvent",
]
# EVENTS
from typing import Any, Dict, List, Optional
from pydantic import Field, field_validator
from mcaddon.core.base import BaseModel
from mcaddon.library.constants import EventTarget, VibrationType, EquipmentSlot
from mcaddon.library.filter import Filter


class EntityRemoveComponent(BaseModel):
    component_groups: List[str] = Field(default_factory=list)


class EntityAddComponent(BaseModel):
    component_groups: List[str] = Field(default_factory=list)


class EmitVibration(BaseModel):
    vibration: VibrationType

    @field_validator("vibration", mode="before")
    @classmethod
    def coerce_enum(cls, v):
        return VibrationType.parse(v)


class PlaySoundEvent(BaseModel):
    sound: str


class EmitParticleEvent(BaseModel):
    particle: str


class EntityTriggerEvent(BaseModel):
    event: Optional[str] = None
    filters: List[Filter] | Filter = Field(default_factory=list)
    filter: Optional[EventTarget] = None
    target: Optional[EventTarget] = None

    @field_validator("target", mode="before")
    @classmethod
    def coerce_enum(cls, v):
        return EventTarget.parse(v)


class EntityDropItem(BaseModel):
    slot: EquipmentSlot

    @field_validator("slot", mode="before")
    @classmethod
    def coerce_enum(cls, v):
        return EquipmentSlot.parse(v)


class EntityQueueCommand(BaseModel):
    command: List[str] | str = Field(default_factory=list)

    def add(self, command: str) -> "EntityQueueCommand":
        # Make list if string
        if isinstance(self.command, str):
            self.command = [self.command]
        self.command.append(command)
        return self


class EntityEvent(BaseModel):
    filters: Optional[Filter] = None
    remove: Optional[EntityRemoveComponent | Dict[str, Any]] = None
    add: Optional[EntityAddComponent] = None
    randomize: Optional[List["RandomizeEvent"]] = None
    sequence: Optional[List["SequenceEvent"]] = None
    queue_command: Optional[EntityQueueCommand] = None
    trigger: Optional[str | EntityTriggerEvent] = None
    set_property: Optional[Dict[str, str | int | bool | float]] = None
    emit_vibration: Optional[EmitVibration] = None
    first_valid: Optional[List["EntityEvent"]] = None
    play_sound: Optional[PlaySoundEvent] = None
    emit_particle: Optional[EmitParticleEvent] = None
    drop_item: Optional[EntityDropItem] = None
    reset_target: Optional[Dict[str, Any]] = None
    execute_event_on_home_block: Optional[EntityTriggerEvent] = None
    stop_movement: Optional[Dict[None, None]] = None
    set_home_position: Optional[Dict[None, None]] = None


class SequenceEvent(EntityEvent):
    pass


class RandomizeEvent(EntityEvent):
    weight: Optional[int] = None
