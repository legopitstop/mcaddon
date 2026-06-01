from abc import ABC
from mcaddon.core.base import BaseComponent, BlockLike
from mcaddon.library.constants import (
    ConnectionState,
    PlacementDirectionState,
    PlacementPositionState,
    MultiBlockState,
    DirectionVertical,
)
from typing import List, Set

__all__ = [
    "BlockTrait",
    "BlockPlacementDirectionTrait",
    "BlockPlacementPositionTrait",
    "BlockConnectionTrait",
    "BlockMultiBlockTrait",
]

class BlockTrait(ABC, BaseComponent): ...

class BlockPlacementDirectionTrait(BlockTrait):
    y_rotation_offset: float | None = ...
    enabled_states: Set[PlacementDirectionState] = ...
    blocks_to_corner_with: List[BlockLike] = ...

    def add_state(
        self, state: PlacementDirectionState
    ) -> "BlockPlacementDirectionTrait": ...

class BlockPlacementPositionTrait(BlockTrait):
    enabled_states: Set[PlacementPositionState] = ...

    def add_state(
        self, state: PlacementPositionState
    ) -> "BlockPlacementPositionTrait": ...

class BlockConnectionTrait(BlockTrait):
    enabled_states: Set[ConnectionState] = ...

    def add_state(self, state: ConnectionState) -> "BlockConnectionTrait": ...

@BlockTrait.register
class BlockMultiBlockTrait(BlockTrait):
    enabled_states: Set[MultiBlockState] = ...
    parts: int = ...
    direction: DirectionVertical = ...

    def add_state(self, state: MultiBlockState) -> "BlockMultiBlockTrait": ...
