from .component import ItemComponent
from mcaddon.core.base import BaseModel

__all__ = ["ItemShooterComponent"]

class Ammunition(BaseModel):
    item: str
    search_inventory: bool
    use_in_creative: bool
    use_offhand: bool

class ItemShooterComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_shooter)
    """

    charge_on_draw: bool = ...
    max_draw_duration: float = ...
    scale_power_by_draw_duration: bool = ...
    ammunition: list[Ammunition] = ...
