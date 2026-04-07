from .component import ItemComponent

__all__ = ["ItemDamageAbsorptionComponent"]

class ItemDamageAbsorptionComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_durability_sensor)
    """

    absorbable_causes: list[str] = ...
