from mcaddon import (
    Block,
    BlockGeometryComponent,
    BlockMaterialInstancesComponent,
    BlockMaterialInstance,
    BlockCollisionBoxComponent,
    BlockSelectionBoxComponent,
)

block = Block()
block.description.identifier = "test:on_interact_change_state_block"
block.components.add(BlockGeometryComponent())
block.components.add(
    BlockMaterialInstancesComponent().add(BlockMaterialInstance(texture="stone"))
)
block.components.add(BlockCollisionBoxComponent())
block.components.add(BlockSelectionBoxComponent())
block.save("out/block.json")
