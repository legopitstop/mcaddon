__all__ = ["EntityOffspringComponent", "DenyParentsVariant"]

from typing import ClassVar, List, Dict, Any, Optional

from pydantic import Field

from mcaddon.core.base import BaseModel, NumberRange

from .component import EntityComponent


class DenyParentsVariant(BaseModel):
    chance: float = 0
    max_variant: int = 0
    min_variant: int = 0


class MutationFactor(BaseModel):
    color: float = 0
    extra_variant: float = 0
    variant: float = 0


@EntityComponent.register
class EntityOffspringComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_offspring)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:offspring"

    mutation_strategy: Optional[str] = None
    blend_attributes: bool = True
    inherit_tamed: bool = True
    combine_parent_colors: bool = False
    random_extra_variant_mutation_interval: NumberRange | int = 0
    random_variant_mutation_interval: NumberRange | int = 0
    deny_parents_variant: DenyParentsVariant | List[DenyParentsVariant] = Field(
        default_factory=list
    )
    mutation_factor: List[MutationFactor] | MutationFactor = Field(default_factory=list)
    parent_centric_attribute_blending: List[str] = Field(default_factory=list)
    offspring_pairs: Dict[str, str] = Field(default_factory=dict)
    property_inheritance: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
