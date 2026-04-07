__all__ = ["EntityBossComponent"]

from typing import Optional, ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityBossComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_boss)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:boss"

    hud_range: int = 55
    name: Optional[str] = None
    should_darken_sky: bool = False
