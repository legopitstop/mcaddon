__all__ = [
    "ItemMaxDamageComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from ..component import ItemComponent
from deprecated import deprecated


@deprecated("This component is deprecated, use ItemDurabilityComponent instead.")
@ItemComponent.register
class ItemMaxDamageComponent(ValueComponent, ItemComponent):
    """
    Use minecraft:durability in newer format versions.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:max_damage"

    value: int
