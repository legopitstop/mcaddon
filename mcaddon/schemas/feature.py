import os

from .. import *
from .. import __file__


class FeatureSchem(Schema):
    def load(cls, self: Feature, data: dict):
        self.identifier = data["description"]["identifier"]


class AggregateSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "aggregate.json",
            ),
        )

    def load(cls, self: AggregateFeature, data: dict):
        super().load(self, data)
        self.features = data.pop("features")
        if "early_out" in data:
            self.early_out = data.pop("early_out")


class SequenceSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__), "data", "schemas", "feature", "sequence.json"
            ),
        )

    def load(cls, self: SequenceFeature, data: dict):
        super().load(self, data)
        self.features = data.pop("features")


class BeardsAndShaversSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "beards_and_shavers.json",
            ),
        )

    def load(cls, self: BeardsAndShaversFeature, data: dict):
        super().load(self, data)
        self.places_feature = data.pop("places_feature")
        self.bounding_box_min = Vector3.from_dict(data.pop("bounding_box_min"))
        self.bounding_box_max = Vector3.from_dict(data.pop("bounding_box_max"))
        self.y_delta = data.pop("y_delta")
        self.surface_block_type = data.pop("surface_block_type")
        self.subsurface_block_type = data.pop("subsurface_block_type")
        self.beard_raggedness_min = data.pop("beard_raggedness_min")
        self.beard_raggedness_max = data.pop("beard_raggedness_max")


class CaveCarverSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "cave_carver.json",
            ),
        )

    def load(cls, self: CaveCarverFeature, data: dict):
        super().load(self, data)
        self.fill_with = data.pop("fill_with")
        self.width_modifier = data.pop("width_modifier")
        self.skip_carve_chance = data.pop("skip_carve_chance")


class ConditionalListSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "conditional_list.json",
            ),
        )

    def load(cls, self: ConditionalListFeature, data: dict):
        super().load(self, data)
        self.early_out_scheme = data.pop("early_out_scheme")
        self.conditional_features = [
            ConditionalFeature.from_dict(x) for x in data.pop("conditional_features")
        ]


class FossilSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__), "data", "schemas", "feature", "fossil.json"
            ),
        )

    def load(cls, self: FossilFeature, data: dict):
        super().load(self, data)
        self.ore_block = BlockState.from_dict(data.pop("ore_block"))
        self.max_empty_corners = data.pop("max_empty_corners")


class GeodeSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__), "data", "schemas", "feature", "geode.json"
            ),
        )

    def load(cls, self: GeodeFeature, data: dict):
        super().load(self, data)
        self.filler = BlockState.from_dict(data.pop("filler"))
        self.inner_layer = BlockState.from_dict(data.pop("inner_layer"))
        self.alternate_inner_layer = BlockState.from_dict(
            data.pop("alternate_inner_layer")
        )
        self.middle_layer = BlockState.from_dict(data.pop("middle_layer"))
        self.outer_layer = BlockState.from_dict(data.pop("outer_layer"))
        self.min_outer_wall_distance = data.pop("min_outer_wall_distance")
        self.max_outer_wall_distance = data.pop("max_outer_wall_distance")
        self.min_distribution_points = data.pop("min_distribution_points")
        self.max_distribution_points = data.pop("max_distribution_points")
        self.min_point_offset = data.pop("min_point_offset")
        self.max_point_offset = data.pop("max_point_offset")
        self.max_radius = data.pop("max_radius")
        self.crack_point_offset = data.pop("crack_point_offset")
        self.generate_crack_chance = data.pop("generate_crack_chance")
        self.base_crack_size = data.pop("base_crack_size")
        self.noise_multiplier = data.pop("noise_multiplier")
        self.use_potential_placements_chance = data.pop(
            "use_potential_placements_chance"
        )
        self.use_alternate_layer0_chance = data.pop("use_alternate_layer0_chance")
        self.placements_require_layer0_alternate = data.pop(
            "placements_require_layer0_alternate"
        )
        self.invalid_blocks_threshold = data.pop("invalid_blocks_threshold")
        self.inner_placements = [
            BlockState.from_dict(x) for x in data.pop("inner_placements")
        ]


class GrowingPlantSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "growing_plant.json",
            ),
        )

    def load(cls, self: GrowingPlantFeature, data: dict):
        super().load(self, data)
        self.growth_direction = data.pop("growth_direction")
        self.height_distribution = [
            HeightDistribution.from_dict(x) for x in data.pop("height_distribution")
        ]
        self.body_blocks = [
            GrowingPlantBlock.from_dict(x) for x in data.pop("body_blocks")
        ]
        self.head_blocks = [
            GrowingPlantBlock.from_dict(x) for x in data.pop("head_blocks")
        ]
        if "age" in data:
            self.age = Range.from_dict(data.pop("age"), "range_")
        if "allow_water" in data:
            self.allow_water = data.pop("allow_water")


class NetherCaveCarverSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "nether_cave_carver.json",
            ),
        )

    def load(cls, self: NetherCaveCarverFeature, data: dict):
        super().load(self, data)
        self.fill_with = BlockState.from_dict(data.pop("fill_with"))
        self.width_modifier = data.pop("width_modifier")


class OreSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__), "data", "schemas", "feature", "ore.json"
            ),
        )

    def load(cls, self: OreFeature, data: dict):
        super().load(self, data)
        self.count = data.pop("count")
        if "replace_rules" in data:
            self.replace_rules = [
                ReplaceRule.from_dict(x) for x in data.pop("replace_rules")
            ]
        if "places_block" in data:
            self.places_block = BlockState.from_dict(data.pop("places_block"))


class MultifaceSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "multiface.json",
            ),
        )

    def load(cls, self: MultifaceFeature, data: dict):
        super().load(self, data)
        self.places_block = BlockState.from_dict(data.pop("places_block"))
        self.search_range = data.pop("search_range")
        self.can_place_on_floor = data.pop("can_place_on_floor")
        self.can_place_on_ceiling = data.pop("can_place_on_ceiling")
        self.can_place_on_wall = data.pop("can_place_on_wall")
        self.chance_of_spreading = data.pop("chance_of_spreading")
        self.can_place_on = [BlockState.from_dict(x) for x in data.pop("can_place_on")]


class PartiallyExposedBlobSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "partially_exposed_blob.json",
            ),
        )

    def load(cls, self: PartiallyExposedBlobFeature, data: dict):
        super().load(self, data)
        self.places_block = BlockState.from_dict(data.pop("places_block"))
        self.placement_radius_around_floor = data.pop("placement_radius_around_floor")
        self.placement_probility_per_valid_position = data.pop(
            "placement_probability_per_valid_position"
        )
        self.exposed_face = data.pop("exposed_face")


class RectLayoutSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "rect_layout.json",
            ),
        )

    def load(cls, self: RectLayoutFeature, data: dict):
        super().load(self, data)
        self.ratio_of_empty_space = data.pop("ratio_of_empty_space")
        self.feature_areas = [
            FeatureArea.from_dict(x) for x in data.pop("feature_areas")
        ]


class ScanSurfaceSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "scan_surface.json",
            ),
        )

    def load(cls, self: ScanSurfaceFeature, data: dict):
        super().load(self, data)
        self.scan_surface_feature = data.pop("scan_surface_feature")


class ScatterSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__), "data", "schemas", "feature", "scatter.json"
            ),
        )

    def load(cls, self: ScatterFeature, data: dict):
        super().load(self, data)
        self.places_feature = data.pop("places_feature")
        self.iterations = Molang(data.pop("iterations"))
        if "scatter_chance" in data:
            self.scatter_chance = data.pop("scatter_chance")

        if isinstance(data["x"], dict):
            self.x = DistributionProvider.from_dict(data.pop("x"))
        elif isinstance(data["x"], list):
            self.x = Vector2(*data.pop("x"))
        else:
            self.x = data.pop("x")

        if isinstance(data["y"], dict):
            self.y = DistributionProvider.from_dict(data.pop("y"))
        elif isinstance(data["y"], list):
            self.y = Vector2(*data.pop("y"))
        else:
            self.y = data.pop("y")

        if isinstance(data["z"], dict):
            self.z = DistributionProvider.from_dict(data.pop("z"))
        elif isinstance(data["z"], list):
            self.z = Vector2(*data.pop("z"))
        else:
            self.z = data.pop("z")


class SculkPatchSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "sculk_patch.json",
            ),
        )

    def load(cls, self: SculkPatchFeature, data: dict):
        super().load(self, data)
        self.can_place_sculk_patch_on = [
            BlockState.from_dict(x) for x in data.pop("can_place_sculk_patch_on")
        ]
        self.central_block = BlockState.from_dict(data.pop("central_block"))
        self.central_block_placement_chance = data.pop("central_block_placement_chance")
        self.charge_amount = data.pop("charge_amount")
        self.cursor_count = data.pop("cursor_count")
        self.growth_rounds = data.pop("growth_rounds")
        self.spread_attempts = data.pop("spread_attempts")
        self.spread_rounds = data.pop("spread_rounds")
        if "extra_growth_chance" in data:
            self.extra_growth_chance = Range.from_dict(
                data.pop("extra_growth_chance"), "range_"
            )


class SearchSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__), "data", "schemas", "feature", "search.json"
            ),
        )

    def load(cls, self: SearchFeature, data: dict):
        super().load(self, data)
        self.places_feature = data.pop("places_feature")
        self.search_volume = VectorRange.from_dict(data.pop("search_volume"))
        self.search_axis = data.pop("search_axis")
        self.required_successes = data.pop("required_successes")


class SingleBlockSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "single_block.json",
            ),
        )

    def load(cls, self: SingleBlockFeature, data: dict):
        super().load(self, data)
        self.places_block = BlockState.from_dict(data.pop("places_block"))
        if "may_replace" in data:
            self.may_replace = [
                BlockState.from_dict(x) for x in data.pop("may_replace")
            ]
        if "may_place_on" in data:
            self.may_place_on = [
                BlockState.from_dict(x) for x in data.pop("may_place_on")
            ]
        if "enforce_survivability_rule" in data:
            self.enforce_survivability_rule = data.pop("enforce_survivability_rule")
        if "enforce_placement_rule" in data:
            self.enforce_placement_rule = data.pop("enforce_placement_rule")


class SnapToSurfaceSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "snap_to_surface.json",
            ),
        )

    def load(cls, self: SnapToSurfaceFeature, data: dict):
        super().load(self, data)
        self.feature_to_snap = data.pop("feature_to_snap")
        self.vertical_search_range = data.pop("vertical_search_range")
        self.surface = data.pop("surface")


class StructureTemplateSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "structure_template.json",
            ),
        )

    def load(cls, self: StructureTemplateFeature, data: dict):
        super().load(self, data)
        self.structure_name = data.pop("structure_name")
        self.adjustment_radius = data.pop("adjustment_radius")
        self.facing_direction = data.pop("facing_direction")
        self.constraints = Constraints.from_dict(data.pop("constraints"))


class SurfaceRelativeThresholdSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "surface_relative_threshold.json",
            ),
        )

    def load(cls, self: SurfaceRelativeThresholdFeature, data: dict):
        super().load(self, data)
        self.minimum_distance_below_surface = data.pop("minimum_distance_below_surface")
        if "feature_to_snap" in data:
            self.feature_to_snap = data.pop("feature_to_snap")


class UnderwaterCaveCarverSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "underwater_cave_carver.json",
            ),
        )

    def load(cls, self: UnderwaterCaveCarverFeature, data: dict):
        super().load(self, data)
        self.fill_with = BlockState.from_dict(data.pop("fill_with"))
        self.width_modifier = data.pop("width_modifier")
        self.replace_air_with = BlockState.from_dict(data.pop("replace_air_with"))


class TreeSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__), "data", "schemas", "feature", "tree.json"
            ),
        )

    def load(cls, self: TreeFeature, data: dict):
        super().load(self, data)
        self.base_block = (
            [BlockState.from_dict(x) for x in data.pop("base_block")]
            if isinstance(data["base_block"], list)
            else [BlockState.from_dict(data.pop("base_block"))]
        )
        if "base_cluster" in data:
            self.base_cluster = Cluster.from_dict(data.pop("base_cluster"))
        if "may_grow_on" in data:
            self.may_grow_on = [
                BlockPredicate.from_dict(x) for x in data.pop("may_grow_on")
            ]
        if "may_grow_through" in data:
            self.may_grow_through = [
                BlockPredicate.from_dict(x) for x in data.pop("may_grow_through")
            ]
        self.may_replace = [BlockState.from_dict(x) for x in data.pop("may_replace")]

        for id, v in data.items():
            clazz = INSTANCE.get_registry(Registries.TREE_TRUNK).get(id)
            if clazz is not None:
                self.trunk = clazz.from_dict(v)

            clazz = INSTANCE.get_registry(Registries.TREE_CANOPY).get(id)
            if clazz is not None:
                self.canopy = clazz.from_dict(v)

            clazz = INSTANCE.get_registry(Registries.TREE_ROOT).get(id)
            if clazz is not None:
                self.root = clazz.from_dict(v)


class VegetationPatchSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "vegetation_patch.json",
            ),
        )

    def load(cls, self: VegetationPatchFeature, data: dict):
        super().load(self, data)
        self.replaceable_blocks = [
            BlockState.from_dict(x) for x in data.pop("replaceable_blocks")
        ]
        self.ground_block = BlockState.from_dict(data.pop("ground_block"))

        self.vegetation_feature = data.pop("vegetation_feature")
        self.surface = data.pop("surface")
        self.depth = (
            Range.from_dict(data.pop("depth"), "range_")
            if isinstance(data["depth"], dict)
            else data.pop("depth")
        )
        self.vertical_range = data.pop("vertical_range")
        self.vegetation_chance = data.pop("vegetation_chance")
        self.horizontal_radius = Range.from_dict(
            data.pop("horizontal_radius"), "range_"
        )
        self.extra_deep_column_chance = data.pop("extra_deep_column_chance")
        if "extra_deep_block_chance" in data:
            self.extra_deep_block_chance = data.pop("extra_deep_block_chance")
        if "waterlogged" in data:
            self.waterlogged = data.pop("waterlogged")


class WeightedRandomSchem1(FeatureSchem):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "feature",
                "weighted_random.json",
            ),
        )

    def load(cls, self: WeightedRandomFeature, data: dict):
        super().load(self, data)
        self.features = [WeightedFeature.from_dict(x) for x in data.pop("features")]
