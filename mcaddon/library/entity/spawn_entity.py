__all__ = ["EntitySpawnEntityComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field, BaseModel
from mcaddon.library.filter import Filter
from .event import EntityTriggerEvent
from .component import EntityComponent


class SpawnEntity(BaseModel):
    filters: Optional[List[Filter] | Filter] = Field(default_factory=list)
    max_wait_time: Optional[int] = None
    min_wait_time: Optional[int] = None
    num_to_spawn: Optional[int] = None
    should_leash: Optional[bool] = None
    single_use: Optional[bool] = None
    spawn_entity: Optional[str] = None
    spawn_event: Optional[str] = None
    spawn_item: Optional[str] = None
    spawn_item_event: Optional[EntityTriggerEvent] = None
    spawn_method: Optional[str] = None
    spawn_sound: Optional[str] = None


@EntityComponent.register
class EntitySpawnEntityComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_spawn_entity)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:spawn_entity"

    entities: List[SpawnEntity] | SpawnEntity = Field(default_factory=list)
    filters: List[Filter] = Field(default_factory=list)
    max_wait_time: int = 600
    min_wait_time: int = 300
    num_to_spawn: int = 1
    should_leash: bool = False
    single_use: bool = False
    spawn_entity: Optional[str] = None
    spawn_event: str = "minecraft:entity_born"
    spawn_item: str = "egg"
    spawn_item_event: Optional[EntityTriggerEvent] = None
    spawn_method: str = "born"
    spawn_sound: str = "plop"
