__all__ = [
    "EntityComponent",
    "EntityAttributeComponent",
    "EntityBehaviorComponent",
    "EntityType",
]

from typing import Optional
from abc import ABC

from mcaddon.core.base import BaseComponent, NumberRange, ValueComponent, BaseModel
from mcaddon.library.filter import Filter
from mcaddon.library.constants import EventTarget


class EntityComponent(ABC, BaseComponent):
    pass


class EntityBehaviorComponent(EntityComponent):
    priority: Optional[int] = None


class EntityAttributeComponent(ValueComponent, EntityComponent):
    value: float | NumberRange = 100
    max: float = 100


class EventTrigger(BaseModel):
    event: Optional[str] = None
    target: Optional[EventTarget] = None
    filters: Optional[Filter] = None


class Range(BaseModel):
    range_min: int
    range_max: int


class EntityType(BaseModel):
    priority: Optional[int] = None
    cooldown: float = 0
    filters: Optional[Filter] = None
    max_dist: float = 16
    must_see: bool = False
    must_see_forget_duration: float = 3
    reevaluate_description: bool = False
    sprint_speed_multiplier: float = 1
    walk_speed_multiplier: float = 1
    check_if_outnumbered: bool = False
    max_flee: Optional[int] = None
