__all__ = ["ItemCameraComponent"]

from typing import ClassVar
from ..component import ItemComponent
from deprecated import deprecated


@deprecated("This component is deprecated.")
@ItemComponent.register
class ItemCameraComponent(ItemComponent):
    COMPONENT_ID: ClassVar[str] = "minecraft:camera"

    black_bars_duration: float
    black_bars_screen_ratio: float
    shutter_duration: float
    picture_duration: float
    slide_away_duration: float
