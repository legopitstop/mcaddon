__all__ = [
    "LegacyBlockRandomTickingComponent",
]

from mcaddon.library.entity.component import EventTrigger

from ..component import BlockComponent
from typing import ClassVar
from deprecated import deprecated


@deprecated("This component is deprecated.")
@BlockComponent.register
class LegacyBlockRandomTickingComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_random_ticking)

    This type is now deprecated, and no longer in use in the latest versions of Minecraft.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:random_ticking"

    on_tick: EventTrigger
