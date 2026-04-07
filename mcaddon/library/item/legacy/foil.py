__all__ = [
    "ItemFoilComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from ..component import ItemComponent
from deprecated import deprecated


@deprecated("This component is deprecated, use ItemGlintComponent instead.")
@ItemComponent.register
class ItemFoilComponent(ValueComponent, ItemComponent):
    """
    Use minecraft:glint in newer format versions.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:foil"

    value: bool
