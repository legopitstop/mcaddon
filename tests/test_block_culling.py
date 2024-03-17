from mcaddon import *

blkcull = BlockCullingRules("test:sushi_cull")
blkcull.add_rule(
    CullingRule(Direction.NORTH, GeometryPart("bb_main", 0, Direction.NORTH))
)
blkcull.add_rule(
    CullingRule(Direction.SOUTH, GeometryPart("bb_main", 0, Direction.SOUTH))
)
blkcull.add_rule(CullingRule(Direction.EAST, GeometryPart("bb_main")))
blkcull.save("build/")
