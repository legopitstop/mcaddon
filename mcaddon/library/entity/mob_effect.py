__all__ = ["EntityMobEffectComponent"]

from typing import Optional, ClassVar
from mcaddon.library.filter import Filter
from .component import EntityComponent


@EntityComponent.register
class EntityMobEffectComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_mob_effect)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:mob_effect"

    mob_effect: str
    ambient: bool = False
    cooldown_time: int = 0
    effect_range: float = 0.2
    effect_time: int = 10
    entity_filter: Optional[Filter] = None
