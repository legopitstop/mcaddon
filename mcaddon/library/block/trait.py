__all__ = [
    "BlockTrait",
    "BlockPlacementDirectionTrait",
    "BlockPlacementPositionTrait",
    "BlockConnectionTrait",
    "BlockMultiBlockTrait",
]

from typing import List, Optional, ClassVar, Set
from pydantic import Field, field_validator
from abc import ABC
from mcaddon.core.base import BaseComponent, BlockLike
from mcaddon.library.constants import (
    PlacementDirectionState,
    PlacementPositionState,
    ConnectionState,
    MultiBlockState,
    DirectionVertical,
)


class BlockTrait(ABC, BaseComponent):
    pass


@BlockTrait.register
class BlockPlacementDirectionTrait(BlockTrait):
    COMPONENT_ID: ClassVar[str] = "minecraft:placement_direction"

    y_rotation_offset: Optional[float] = 0
    enabled_states: Set[PlacementDirectionState] = Field(default_factory=set)
    blocks_to_corner_with: List[BlockLike] = Field(default_factory=list)

    @field_validator("y_rotation_offset")
    @classmethod
    def multiple_of_90(cls, v: float):
        if v % 90 != 0:
            raise ValueError("rotation must be a multiple of 90")
        return v

    def add_state(
        self, state: PlacementDirectionState
    ) -> "BlockPlacementDirectionTrait":
        self.enabled_states.add(state)
        return self


@BlockTrait.register
class BlockPlacementPositionTrait(BlockTrait):
    COMPONENT_ID: ClassVar[str] = "minecraft:placement_position"

    enabled_states: Set[PlacementPositionState] = Field(default_factory=set)

    def add_state(self, state: PlacementPositionState) -> "BlockPlacementPositionTrait":
        self.enabled_states.add(state)
        return self


@BlockTrait.register
class BlockConnectionTrait(BlockTrait):
    COMPONENT_ID: ClassVar[str] = "minecraft:connection"

    enabled_states: Set[ConnectionState] = Field(default_factory=set)

    def add_state(self, state: ConnectionState) -> "BlockConnectionTrait":
        self.enabled_states.add(state)
        return self


@BlockTrait.register
class BlockMultiBlockTrait(BlockTrait):
    COMPONENT_ID: ClassVar[str] = "minecraft:multi_block"

    enabled_states: Set[MultiBlockState] = Field(default_factory=set)
    parts: int = Field(default=1, ge=1)
    direction: DirectionVertical = DirectionVertical.UP

    def add_state(self, state: MultiBlockState) -> "BlockMultiBlockTrait":
        self.enabled_states.add(state)
        return self
