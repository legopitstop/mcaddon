__all__ = [
    "BlockConnectionRuleComponent",
]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.library.constants import Direction2d, Connections
from .component import BlockComponent


@BlockComponent.register
class BlockConnectionRuleComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_connection_rule)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:connection_rule"

    accepts_connections_from: Connections = Connections.ALL
    enabled_directions: List[Direction2d] = Field(default=[dir for dir in Direction2d])
