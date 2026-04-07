__all__ = [
    "STAIRS",
    "DOOR",
    "TRAPDOOR",
    "FENCE",
    "FENCE_GATE",
    "LOG",
    "PRESSURE_PLATE",
    "BUTTON",
    "SLAB",
]

from molang.dsl import query
from mcaddon import (
    Block,
    MenuCategories,
    BlockPlacementDirectionTrait,
    BlockPlacementPositionTrait,
    PlacementDirectionState,
    PlacementPositionState,
    BlockTickComponent,
)
from mcaddon.library.block.base import BlockPermutation
from mcaddon.library.block.collision_box import BlockCollisionBoxComponent
from mcaddon.library.block.geometry import BlockGeometryComponent
from mcaddon.library.block.liquid_detection import (
    BlockLiquidDetectionComponent,
    DetectionRule,
)
from mcaddon.library.block.selection_box import BlockSelectionBoxComponent
from mcaddon.library.block.transformation import BlockTransformationComponent
from mcaddon.library.constants import DirectionAll

STAIRS = Block()
STAIRS.description.identifier = "mcaddon:stairs"
STAIRS.description.menu_category = MenuCategories.STAIRS
STAIRS.description.add_trait(
    BlockPlacementDirectionTrait(y_rotation_offset=180).add_state(
        PlacementDirectionState.CARDINAL_DIRECTION
    )
)
STAIRS.description.add_trait(
    BlockPlacementPositionTrait().add_state(PlacementPositionState.VERTICAL_HALF)
)
STAIRS.description.add_state(
    "mcaddon:shape",
    ["straight", "inner_left", "inner_right", "outer_left", "outer_right"],
)
STAIRS.components.add(BlockTickComponent())
STAIRS.components.add(BlockCollisionBoxComponent(origin=(-8, 0, -8), size=(8, 8, 8)))
STAIRS.permutations.append(
    BlockPermutation(
        condition=query.block_state("minecraft:vertical_half") == "top"
    ).add(BlockCollisionBoxComponent(origin=(-8, 8, -8), size=(16, 8, 16))),
)
STAIRS.permutations.append(
    BlockPermutation(
        condition=(query.block_state("minecraft:cardinal_direction") == "north")
        & query.block_state("minecraft:vertical_half")
        == "bottom"
    )
    .add(BlockTransformationComponent().rotate((0, -90, 0)))
    .add(
        BlockLiquidDetectionComponent().add(
            DetectionRule(can_contain_liquid=True).add(DirectionAll.SOUTH)
        )
    )
)
STAIRS.permutations.append(
    BlockPermutation(
        condition=(query.block_state("minecraft:cardinal_direction") == "south")
        & query.block_state("minecraft:vertical_half")
        == "bottom"
    )
    .add(BlockTransformationComponent().rotate((0, 90, 0)))
    .add(
        BlockLiquidDetectionComponent().add(
            DetectionRule(can_contain_liquid=True).add(DirectionAll.NORTH)
        )
    )
)
STAIRS.permutations.append(
    BlockPermutation(
        condition=(query.block_state("minecraft:cardinal_direction") == "east")
        & query.block_state("minecraft:vertical_half")
        == "bottom"
    )
    .add(BlockTransformationComponent().rotate((0, 180, 0)))
    .add(
        BlockLiquidDetectionComponent().add(
            DetectionRule(can_contain_liquid=True).add(DirectionAll.WEST)
        )
    )
)
STAIRS.permutations.append(
    BlockPermutation(
        condition=(query.block_state("minecraft:cardinal_direction") == "west")
        & query.block_state("minecraft:vertical_half")
        == "bottom"
    )
    .add(BlockTransformationComponent().rotate((0, 0, 0)))
    .add(
        BlockLiquidDetectionComponent().add(
            DetectionRule(can_contain_liquid=True).add(DirectionAll.EAST)
        )
    )
)
STAIRS.permutations.append(
    BlockPermutation(
        condition=(query.block_state("minecraft:cardinal_direction") == "north")
        & query.block_state("minecraft:vertical_half")
        == "top"
    )
    .add(BlockTransformationComponent().rotate((180, -90, 0)))
    .add(
        BlockLiquidDetectionComponent().add(
            DetectionRule(can_contain_liquid=True).add(DirectionAll.SOUTH)
        )
    )
)
STAIRS.permutations.append(
    BlockPermutation(
        condition=(query.block_state("minecraft:cardinal_direction") == "south")
        & query.block_state("minecraft:vertical_half")
        == "top"
    )
    .add(BlockTransformationComponent().rotate((180, 90, 0)))
    .add(
        BlockLiquidDetectionComponent().add(
            DetectionRule(can_contain_liquid=True).add(DirectionAll.NORTH)
        )
    )
)
STAIRS.permutations.append(
    BlockPermutation(
        condition=(query.block_state("minecraft:cardinal_direction") == "east")
        & query.block_state("minecraft:vertical_half")
        == "top"
    )
    .add(BlockTransformationComponent().rotate((180, 180, 0)))
    .add(
        BlockLiquidDetectionComponent().add(
            DetectionRule(can_contain_liquid=True).add(DirectionAll.WEST)
        )
    )
)
STAIRS.permutations.append(
    BlockPermutation(
        condition=(query.block_state("minecraft:cardinal_direction") == "west")
        & query.block_state("minecraft:vertical_half")
        == "top"
    )
    .add(BlockTransformationComponent().rotate((180, 0, 0)))
    .add(
        BlockLiquidDetectionComponent().add(
            DetectionRule(can_contain_liquid=True).add(DirectionAll.EAST)
        )
    )
)


SLAB = Block()
SLAB.description.identifier = "mcaddon:slab"
SLAB.description.menu_category = MenuCategories.SLAB
SLAB.description.add_state("mcaddon:double", [False, True])
SLAB.description.add_trait(
    BlockPlacementPositionTrait().add_state(PlacementPositionState.VERTICAL_HALF)
)
SLAB.components.add(
    BlockLiquidDetectionComponent().add(DetectionRule(can_contain_liquid=False))
)
SLAB.permutations.append(
    BlockPermutation(condition=query.block_state("mcaddon:double"))
    .add(BlockGeometryComponent(identifier="minecraft:geometry.full_block"))
    .add(BlockCollisionBoxComponent(origin=(-8, 8, -8), size=(16, 8, 16)))
    .add(BlockSelectionBoxComponent(origin=(-8, 8, -8), size=(16, 8, 16)))
)
SLAB.permutations.append(
    BlockPermutation(
        condition=~query.block_state("mcaddon:double")
        & query.block_state("minecraft:vertical_half")
        == "top"
    ).add(
        BlockLiquidDetectionComponent().add(
            DetectionRule(can_contain_liquid=True).add(DirectionAll.UP)
        )
    )
)
SLAB.permutations.append(
    BlockPermutation(
        condition=~query.block_state("mcaddon:double")
        & query.block_state("minecraft:vertical_half")
        == "bottom"
    )
    .add(BlockCollisionBoxComponent(origin=(-8, 8, -8), size=(16, 8, 16)))
    .add(BlockSelectionBoxComponent(origin=(-8, 8, -8), size=(16, 8, 16)))
    .add(
        BlockLiquidDetectionComponent().add(
            DetectionRule(can_contain_liquid=True).add(DirectionAll.DOWN)
        )
    )
)


DOOR = Block()
DOOR.description.identifier = "mcaddon:door"
DOOR.description.menu_category = MenuCategories.DOOR

TRAPDOOR = Block()
TRAPDOOR.description.identifier = "mcaddon:trapdoor"
TRAPDOOR.description.menu_category = MenuCategories.TRAPDOOR


FENCE = Block()
FENCE.description.identifier = "mcaddon:fence"
FENCE.description.menu_category = MenuCategories.FENCE


FENCE_GATE = Block()
FENCE_GATE.description.identifier = "mcaddon:fence_gate"
FENCE_GATE.description.menu_category = MenuCategories.FENCE_GATE


LOG = Block()
LOG.description.identifier = "mcaddon:log"
LOG.description.menu_category = MenuCategories.LOG


PRESSURE_PLATE = Block()
PRESSURE_PLATE.description.identifier = "mcaddon:pressure_plate"
PRESSURE_PLATE.description.menu_category = MenuCategories.PRESSURE_PLATE


BUTTON = Block()
BUTTON.description.identifier = "mcaddon:button"
BUTTON.description.menu_category = MenuCategories.BUTTONS
