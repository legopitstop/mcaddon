__all__ = [
    "ItemThrowableComponent",
]

from typing import ClassVar
from .component import ItemComponent


@ItemComponent.register
class ItemThrowableComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_throwable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:throwable"

    do_swing_animation: bool = False
    launch_power_scale: float = 1
    max_draw_duration: float = 0
    max_launch_power: float = 1
    min_draw_duration: float = 0
    scale_power_by_draw_duration: bool = False
