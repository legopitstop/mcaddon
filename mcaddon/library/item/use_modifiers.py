__all__ = [
    "ItemUseModifiersComponent",
]

from typing import ClassVar
from typing import Optional
from .component import ItemComponent


@ItemComponent.register
class ItemUseModifiersComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_use_modifiers)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:use_modifiers"

    emit_vibrations: bool = True
    movement_modifier: Optional[float] = None
    use_duration: float = 0
    start_sound: Optional[str] = None
