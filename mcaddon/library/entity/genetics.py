__all__ = ["EntityGeneticsComponent", "GeneticVariant", "Genes"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel, NumberRange
from .event import EntityTriggerEvent
from .component import EntityComponent


class GeneticVariant(BaseModel):
    birth_event: Optional[EntityTriggerEvent] = None
    both_allele: int | NumberRange = -1
    either_allele: int | NumberRange = -1
    hidden_allele: int | NumberRange = -1
    main_allele: int | NumberRange = -1


class Genes(BaseModel):
    allele_range: Optional[NumberRange | int] = None
    genetic_variants: List[GeneticVariant] = Field(default_factory=list)
    mutation_rate: float = -1
    name: Optional[str] = None
    use_simplified_breeding: Optional[bool] = None


@EntityComponent.register
class EntityGeneticsComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_genetics)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:genetics"

    genes: List[Genes] = Field(default_factory=list)
    mutation_rate: float = 0.03125
