__all__ = ["EntityMobEffectImmunityComponent"]

from typing import List, ClassVar
from pydantic import Field
from .component import EntityComponent


@EntityComponent.register
class EntityMobEffectImmunityComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_mob_effect_immunity)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:mob_effect_immunity"

    mob_effects: List[str] = Field(default_factory=list)
