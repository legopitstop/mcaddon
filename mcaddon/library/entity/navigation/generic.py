__all__ = ["EntityNavigationGenericComponent"]

from typing import Optional, List, ClassVar
from mcaddon.core.base import BlockLike
from mcaddon.library.entity.component import EntityComponent


@EntityComponent.register
class EntityNavigationGenericComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_navigation.generic)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:navigation.generic"

    using_door_annotation: bool = False
    avoid_damage_blocks: bool = False
    avoid_portals: bool = False
    avoid_sun: bool = False
    avoid_water: bool = False
    blocks_to_avoid: Optional[List[BlockLike]] = None
    can_breach: bool = False
    can_break_doors: bool = False
    can_jump: bool = False
    can_open_doors: bool = False
    can_open_iron_doors: bool = False
    can_pass_doors: bool = True
    can_path_from_air: bool = False
    can_path_over_lava: bool = False
    can_path_over_water: bool = False
    can_sink: bool = True
    can_swim: bool = False
    can_walk: bool = True
    can_walk_in_lava: bool = False
    is_amphibious: bool = False
