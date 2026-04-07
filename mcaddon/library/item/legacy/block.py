__all__ = [
    "ItemBlockComponent",
]

from typing import ClassVar

from mcaddon.core.base import ValueComponent
from ..component import ItemComponent
from deprecated import deprecated


@deprecated("This component is deprecated, use ItemBlockPlacerComponent instead.")
@ItemComponent.register
class ItemBlockComponent(ValueComponent, ItemComponent):
    """
    Use minecraft:block_placer in newer format versions.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:block"  # noqa: F821

    value: str
