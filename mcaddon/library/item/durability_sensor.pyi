from .component import ItemComponent

__all__ = ["ItemDurabilitySensorComponent"]

class ItemDurabilitySensorComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_durability_sensor)
    """

    durability: int = ...
    particle_type: str | None = ...
    sound_event: str | None = ...
