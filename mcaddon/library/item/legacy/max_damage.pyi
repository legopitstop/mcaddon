from ..component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemMaxDamageComponent"]

class ItemMaxDamageComponent(ValueComponent, ItemComponent):
    """
    Use minecraft:durability in newer format versions.
    """

    value: int
