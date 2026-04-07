__all__ = ["EntityBreedableComponent"]

from typing import List, Optional, Dict, Any, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel, NumberRange, ItemResult
from mcaddon.library.filter import FilterTest
from .event import EntityTriggerEvent
from .component import EntityComponent


class BreedsWith(BaseModel):
    baby_type: Optional[str] = None
    mate_type: Optional[str] = None
    breed_event: Optional[EntityTriggerEvent] = None


class DenyParentsVariant(BaseModel):
    chance: float
    max_variant: int
    min_variant: int


class EnvironmentRequirement(BaseModel):
    block_types: List[str] = Field(default_factory=list)
    blocks: List[str] | str = Field(default_factory=list)
    count: int = 1
    radius: float = 5


class MutationFactor(BaseModel):
    color: float = 0
    extra_variant: float = 0
    variant: float = 0


@EntityComponent.register
class EntityBreedableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_breedable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:breedable"

    allow_sitting: bool = False
    blend_attributes: bool = True
    breed_cooldown: float = 60
    breed_items: List[str | ItemResult] | str = Field(default_factory=list)
    breeds_with: List[BreedsWith] | Dict[str, EntityTriggerEvent] | BreedsWith = Field(
        default_factory=list
    )
    causes_pregnancy: bool = False
    combine_parent_colors: Optional[bool] = None
    deny_parents_variant: Optional[DenyParentsVariant] = None
    environment_requirements: List[EnvironmentRequirement] | EnvironmentRequirement = (
        Field(default_factory=list)
    )
    extra_baby_chance: int = 0
    inherit_tamed: bool = True
    love_filters: Optional[FilterTest] = None
    mutation_factor: Optional[MutationFactor] = None
    mutation_strategy: Optional[str] = None
    parent_centric_attribute_blending: List[str] = Field(default_factory=list)
    property_inheritance: List[str] | Dict[str, Any] = Field(default_factory=list)
    random_extra_variant_mutation_interval: int | NumberRange = 0
    random_variant_mutation_interval: int | NumberRange = 0
    require_full_health: bool = False
    require_tame: bool = True
    transform_to_item: Optional[str] = None
