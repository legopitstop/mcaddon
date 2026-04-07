__all__ = ["EntitySpellEffectsComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from .component import EntityComponent


class AddEffects(BaseModel):
    display_on_screen_animation: Optional[bool] = None
    duration: Optional[float] = None
    effect: Optional[str] = None


@EntityComponent.register
class EntitySpellEffectsComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_spell_effects)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:spell_effects"

    add_effects: List[AddEffects] = Field(default_factory=list)
    remove_effects: Optional[List[str] | str] = None
