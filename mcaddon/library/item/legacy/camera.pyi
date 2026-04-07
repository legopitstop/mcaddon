from ..component import ItemComponent

__all__ = ["ItemCameraComponent"]

class ItemCameraComponent(ItemComponent):
    black_bars_duration: float
    black_bars_screen_ratio: float
    shutter_duration: float
    picture_duration: float
    slide_away_duration: float
