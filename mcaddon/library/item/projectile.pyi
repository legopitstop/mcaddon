from .component import ItemComponent

__all__ = ["ItemProjectileComponent"]

class ItemProjectileComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_projectile)
    """

    projectile_entity: str
    minimum_critical_power: float = ...
