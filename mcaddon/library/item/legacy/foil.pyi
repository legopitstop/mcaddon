from ..component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemFoilComponent"]

class ItemFoilComponent(ValueComponent, ItemComponent):
    """
    Use minecraft:glint in newer format versions.
    """

    value: bool
