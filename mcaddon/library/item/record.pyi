from .component import ItemComponent

__all__ = ["ItemRecordComponent"]

class ItemRecordComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_record)
    """

    sound_event: str
    comparator_signal: int = ...
    duration: float = ...
