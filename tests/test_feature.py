from mcaddon import *


# Features

fea1 = AggregateFeature("example:monument_with_flowers_feature")
fea1.add_feature("monument_feature")
fea1.add_feature("scatter_white_flowers_feature")
fea1.add_feature("scatter_yellow_flower_feature")
fea1.save("build/")

fea2 = SequenceFeature("example:oak_tree_then_apples_feature")
fea2.add_feature("oak_tree_feature")
fea2.add_feature("scatter_apples_feature")
fea2.save("build/")

fea3 = BeardsAndShaversFeature(
    "code:beards_and_shavers",
    "minecraft:feature_that_places_a_structure",
    Vector3(-2, 0, -2),
    Vector3(2, 8, 2),
    2.0,
    "grass",
    "dirt",
    0.1,
    0.3,
)
fea3.save("build/")

fea4 = CaveCarverFeature("minecraft:underground_cave_carver_feature", "air", 0.0, 15)
fea4.save("build/")

fea5 = ConditionalListFeature("test:conditional_features", "placement_success")
fea5.add_feature(
    ConditionalFeature(
        "minecraft:some_feature_or_other", Molang("query.check_some_block_property()")
    )
)
fea5.save("build/")

fea6 = FossilFeature("minecraft:fossil_feature", "coal_ore", 4)
fea6.save("build/")

fea7 = GeodeFeature(
    "minecraft:diamond_geode_feature",
    "air",
    "diamond_block",
    "emerald_block",
    "calcite",
    "obsidian",
    4,
    7,
    3,
    5,
    1,
    3,
    16,
    2.0,
    0.95,
    2.0,
    0.025,
    0.35,
    0.0083,
    True,
    1,
)
fea7.add_placement(BlockState("amethyst_cluster", {"amethyst_cluster_type": "small"}))
fea7.save("build/")

fea8 = GrowingPlantFeature("minecraft:cave_vine_feature", "DOWN", True, Range(17, 26))
fea8.add_height_distribution(HeightDistribution(Range(1, 13), 2))
fea8.add_height_distribution(HeightDistribution(Range(1, 2), 3))
fea8.add_height_distribution(HeightDistribution(Range(1, 7), 10))
fea8.add_body_block(GrowingPlantBlock("cave_vines", 4))
fea8.add_body_block(GrowingPlantBlock("cave_vines_body_with_berries", 1))
fea8.add_head_block(GrowingPlantBlock("cave_vines", 4))
fea8.add_head_block(GrowingPlantBlock("cave_vines_head_with_berries", 1))
fea8.save("build/")

fea9 = NetherCaveCarverFeature("minecraft:nether_cave_carver_feature", "air", 0.0)
fea9.save("build/")

fea10 = MultifaceFeature(
    "example:blue_vines_feature", "example:blue_vine", 64, True, True, True, 0.5
)
fea10.add_place_on_block("stone")
fea10.save("build/")

fea11 = OreFeature("example:malachite_ore_feature", 12)
fea11.add_rule(ReplaceRule("example:malachite_ore", ["stone"]))
fea11.add_rule(ReplaceRule("example:granite_malachite_ore", ["granite"]))
fea11.add_rule(ReplaceRule("example:andesite_malachite_ore", ["andesite"]))
fea11.save("build/")

fea12 = PartiallyExposedBlobFeature(
    "example:underwater_magma_feature", "magma", 1, 0.5, "up"
)
fea12.save("build/")

fea13 = RectLayoutFeature("example:rect_layout_feature", 0.5)
fea13.add_feature_area(FeatureArea("tree", Vector2(0, 0)))
fea13.add_feature_area(FeatureArea("tree2", Vector2(0, 0)))
fea13.save("build/")

fea14 = ScanSurfaceFeature("example:scan_surface_feature", "example:apple_feature")
fea14.save("build/")

fea15 = ScatterFeature(
    "example:scatter_flowers_feature",
    "example:flower_feature",
    10,
    x=DistributionProvider("uniform", Vector2(0, 15)),
    y=64,
    z=DistributionProvider("uniform", Vector2(0, 15)),
    scatter_chance=50.0,
)
fea15.save("build/")

fea16 = SculkPatchFeature(
    "example:sculk_patch_feature", "stone", 1.0, 1, 1, 1, 1, 1, Range(1, 5)
)
fea16.add_can_place_on("stone")
fea16.save("build/")

fea17 = SearchFeature(
    "example:find_valid_apples_feature",
    "example:apple_feature",
    VectorRange(Vector3(-3, -3, -3), Vector3(3, 3, 3)),
    "-y",
    3,
)
fea17.save("build/")

fea18 = SingleBlockFeature(
    "example:single_pumpkin_feature", "example:pumpkin", True, True
)
fea18.add_place_on("example:grass")
fea18.add_replace("example:air")
fea18.save("build/")

fea19 = SnapToSurfaceFeature(
    "minecraft:cave_vine_snapped_to_ceiling_feature",
    "minecraft:cave_vine_feature",
    12,
    "ceiling",
)
fea19.save("build/")

bi = BlockIntersection()
bi.add_allow_block("example:air")
fea20 = StructureTemplateFeature(
    "example:hot_air_balloon_feature",
    "example:hot_air_balloon",
    8,
    "random",
    Constraints(True, bi),
)
fea20.save("build/")

fea21 = SurfaceRelativeThresholdFeature(
    "minecraft:underwater_magma_underground_feature",
    "minecraft:underwater_magma_snap_to_surface_feature",
    2,
)
fea21.save("build/")

fea22 = UnderwaterCaveCarverFeature(
    "minecraft:underground_cave_carver_feature", "water", 0.0, "flowing_water"
)
fea22.save("build/")

# TODO: https://bedrock.dev/docs/stable/Features#minecraft%3Atree_feature

at = AcaciaTrunk(
    BlockState("log", {"old_log_type": "oak"}),
    TrunkHeight(4, [2], 3),
    1,
    TrunkLean(True, Range(2, 3), Range(3, 4), Range(1, 2)),
)
rsc = RandomSpreadCanopy(2, 3, 50)
rsc.add_leaf(WeightedBlock("azalea_leaves", 3))
rsc.add_leaf(WeightedBlock("azalea_leaves_flowered", 1))
fea23 = TreeFeature("custom:azalea_tree_feature", at, rsc)
fea23.add_base_block("dirt_with_roots")
fea23.add_grow_on("dirt")
fea23.add_grow_on("grass")
fea23.add_grow_on("podzol")
fea23.add_grow_on("dirt")
fea23.add_grow_on("farmland")
fea23.add_grow_on("dirt_with_roots")
fea23.add_grow_on("moss_block")
fea23.add_grow_on("clay")
fea23.add_grow_on("mycelium")
fea23.add_grow_on("mud")
fea23.add_grow_on("muddy_mangrove_roots")
fea23.add_replace("leaves")
fea23.add_replace("leaves2")
fea23.add_replace("azalea")
fea23.add_replace("flowering_azalea")
fea23.add_replace("azalea_leaves")
fea23.add_replace("azalea_leaves_flowered")
fea23.add_replace("mangrove_leaves")
fea23.add_replace("water")
fea23.add_replace("flower_water")
fea23.add_replace("moss_carpet")
fea23.add_replace("tallgrass")
fea23.add_replace("grass")
fea23.add_replace("air")
fea23.add_replace("double_plant")
fea23.add_grow_through("dirt")
fea23.add_grow_through("grass")
fea23.add_grow_through("moss_carpet")
fea23.add_grow_through("tallgrass")
fea23.add_grow_through("double_plant")
fea23.save("build/")

fea24 = VegetationPatchFeature(
    "custom:clay_pool_with_dripleaves_feature",
    "clay",
    "dripleaf_feature",
    "floor",
    3,
    5,
    0.1,
    Range(4, 8),
    0.8,
    0.7,
    True,
)
fea24.add_replace("clay")
fea24.add_replace("moss_block")
fea24.add_replace("sand")
fea24.add_replace("gravel")
fea24.add_replace("dirt")
fea24.add_replace("podzol")
fea24.add_replace("dirt_with_roots")
fea24.add_replace("grass")
fea24.add_replace("mycelium")
fea24.add_replace("stone")
fea24.add_replace("cave_vines")
fea24.add_replace("cave_vines_body_with_berries")
fea24.add_replace("cave_vines_head_with_berries")
fea24.save("build/")

features = [
    fea1,
    fea2,
    fea3,
    fea4,
    fea5,
    fea6,
    fea7,
    fea8,
    fea9,
    fea10,
    fea11,
    fea12,
    fea13,
    fea14,
    fea15,
    fea16,
    fea17,
    fea18,
    fea19,
    fea20,
    fea21,
    fea22,
    fea23,
    fea24,
]
