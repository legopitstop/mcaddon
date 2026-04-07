__all__ = [
    "ItemMenuCategoryComponent",
]

from typing import ClassVar, Optional

from mcaddon.core.base import ValueComponent
from mcaddon.library.constants import CreativeCategory
from ..component import ItemComponent
from deprecated import deprecated


@deprecated("This component is deprecated, use Item.description.menu_category instead.")
@ItemComponent.register
class ItemMenuCategoryComponent(ValueComponent, ItemComponent):
    """
    Use minecraft:item.description.menu_category in newer format versions.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:menu_category"

    category: Optional[CreativeCategory]
    group: Optional[str] = None
