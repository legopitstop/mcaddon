from ..component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemBlockComponent"]

class ItemBlockComponent(ValueComponent, ItemComponent):
    """
    Use minecraft:block_placer in newer format versions.
    """

    value: str
