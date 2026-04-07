__all__ = [
    "BlockFlammableComponent",
]


from .component import BlockComponent
from typing import ClassVar


@BlockComponent.register
class BlockFlammableComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_flammable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:flammable"

    catch_chance_modifier: int = 5
    destroy_chance_modifier: int = 20
