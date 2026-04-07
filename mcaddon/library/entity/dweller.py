__all__ = ["EntityDwellerComponent", "DwellerRole"]

from typing import Optional, ClassVar
from mcaddon.library.constants import DwellerRole
from .component import EntityComponent


@EntityComponent.register
class EntityDwellerComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_dweller)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:dweller"

    can_find_poi: Optional[bool] = None
    can_migrate: Optional[bool] = None
    dweller_role: Optional[DwellerRole] = None
    dwelling_bounds_tolerance: Optional[float] = None
    dwelling_role: Optional[str] = None
    dwelling_type: Optional[str] = "village"
    first_founding_reward: Optional[int] = None
    preferred_profession: Optional[str] = None
    update_interval_base: Optional[float] = None
    update_interval_variant: Optional[float] = None
