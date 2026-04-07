from .component import ItemComponent

__all__ = ["ItemSwingSoundsComponent"]

class ItemSwingSoundsComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_swing_sounds)
    """

    attack_critical_hit: str | None = ...
    attack_hit: str | None = ...
    attack_miss: str | None = ...
