from .component import BlockComponent
from mcaddon.library.constants import Connections, Direction2d

__all__ = ["BlockConnectionRuleComponent"]

class BlockConnectionRuleComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_connection_rule)
    """

    accepts_connections_from: Connections
    enabled_directions: list[Direction2d]
