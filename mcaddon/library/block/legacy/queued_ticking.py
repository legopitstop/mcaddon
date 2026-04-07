__all__ = [
    "LegacyBlockQueuedTickingComponent",
]

from mcaddon.core.base import NumberRange
from mcaddon.library.entity.component import EventTrigger
from ..component import BlockComponent
from typing import ClassVar
from deprecated import deprecated


@deprecated("This component is deprecated, use BlockTickComponent instead.")
@BlockComponent.register
class LegacyBlockQueuedTickingComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_queued_ticking)

    This type is now deprecated, and no longer in use in the latest versions of Minecraft.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:queued_ticking"

    interval_range: NumberRange
    looping: bool
    on_tick: EventTrigger
