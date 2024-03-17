from typing import Self
from molang import Molang
from dataclasses import dataclass

from . import VERSION
from .exception import TypeNotFoundError
from .registry import INSTANCE, Registries
from .pack import behavior_pack
from .math import Range, Slope, Vector3, Vector2, VectorRange, Chance
from .util import getattr2, Identifier, Identifiable
from .file import JsonFile, Loader
from .block import BlockState, BlockPredicate

# TODO: Add on_update to all properties


class Feature(JsonFile, Identifiable):
    """
    Represents a data-driven [Feature](https://bedrock.dev/docs/stable/Features).
    """

    def __init__(self, identifier: Identifiable):
        Identifiable.__init__(self, identifier)

    def __str__(self) -> str:
        return self.__class__.__name__ + "{" + str(self.identifier) + "}"

    def jsonify(self) -> dict:
        data = {
            "format_version": VERSION["FEATURE"],
            str(self.id): {"description": {"identifier": str(self.identifier)}},
        }
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        for k, v in INSTANCE.get_registry(Registries.FEATURE_TYPE).items():
            if str(k) in data:
                self = v.from_dict(data)
                dat = data.get(str(self.id))
                self.identifier = dat["description"]["identifier"]
                return self
        raise TypeNotFoundError(data)

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier.of(value))


INSTANCE.create_registry(Registries.FEATURE_TYPE, Feature)


def feature_type(cls):
    """
    Add this feature type to the registry
    """

    def wrapper():
        return INSTANCE.register(Registries.FEATURE_TYPE, cls.id, cls)

    return wrapper()


class WeightedBlock:
    def __init__(self, block: BlockState, weight: int):
        self.block = block
        self.weight = weight

    @property
    def block(self) -> BlockState:
        return getattr(self, "_block")

    @block.setter
    def block(self, value: BlockState):
        setattr(self, "_block", BlockState.of(value))

    @property
    def weight(self) -> int:
        return getattr(self, "_weight")

    @weight.setter
    def weight(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_weight", value)

    @staticmethod
    def from_dict(data: list) -> Self:
        return WeightedBlock(*data)

    def jsonify(self) -> dict:
        data = [self.block.jsonify(), self.weight]
        return data


@feature_type
@behavior_pack
class AggregateFeature(Feature):
    """
    Represents a data-driven [Aggregate Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Aaggregate_feature).
    """

    id = Identifier("aggregate_feature")
    FILEPATH = "features/aggregate_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        features: list[Identifiable] = [],
        early_out: str = None,
    ):
        Feature.__init__(self, identifier)
        self.features = features
        self.early_out = early_out

    @property
    def features(self) -> list[Identifier]:
        return getattr(self, "_features")

    @features.setter
    def features(self, value: list[Identifiable]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_features", [Identifiable.of(x) for x in value])

    @property
    def early_out(self) -> str:
        return getattr(self, "_early_out")

    @early_out.setter
    def early_out(self, value: str):
        if value is None:
            return
        setattr(self, "_early_out", str(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = AggregateFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["features"] = [str(x) for x in self.features]
        return data

    # FEATURE

    def get_feature(self, index: int) -> Identifier:
        return self.features[index]

    def add_feature(self, feature: Identifiable) -> Identifiable:
        id = Identifiable.of(feature)
        self.features.append(id)
        return id

    def remove_feature(self, index: int) -> Identifier:
        return self.features.pop(index)

    def clear_features(self) -> Self:
        self.features.clear()
        return self


class AggregateFeatureLoader(Loader):
    name = "Aggregate Feature"

    def __init__(self):
        from .schemas import AggregateSchem1

        Loader.__init__(self, AggregateFeature)
        self.add_schema(AggregateSchem1, "1.13.0")
        self.add_schema(AggregateSchem1, "1.16.0")


@feature_type
@behavior_pack
class SequenceFeature(Feature):
    """
    Represents a data-driven [Sequence Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Asequence_feature).
    """

    id = Identifier("sequence_feature")
    FILEPATH = "features/sequence_feature.json"

    def __init__(self, identifier: Identifiable, features: list[Identifiable] = []):
        Feature.__init__(self, identifier)
        self.features = features

    @property
    def features(self) -> list[Identifier]:
        return getattr(self, "_features")

    @features.setter
    def features(self, value: list[Identifiable]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_features", [Identifiable.of(x) for x in value])

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = SequenceFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["features"] = [str(x) for x in self.features]
        return data

    # FEATURE

    def get_feature(self, index: int) -> Identifier:
        return self.features[index]

    def add_feature(self, feature: Identifiable) -> Identifiable:
        id = Identifiable.of(feature)
        self.features.append(id)
        return id

    def remove_feature(self, index: int) -> Identifier:
        return self.features.pop(index)

    def clear_features(self) -> Self:
        self.features.clear()
        return self


class SequenceFeatureLoader(Loader):
    name = "Sequence Feature"

    def __init__(self):
        from .schemas import SequenceSchem1

        Loader.__init__(self, SequenceFeature)
        self.add_schema(SequenceSchem1, "1.13.0")
        self.add_schema(SequenceSchem1, "1.16.0")


@feature_type
@behavior_pack
class BeardsAndShaversFeature(Feature):
    """
    Represents a data-driven [Beards And Shavers Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Abeards_and_shavers).
    """

    id = Identifier("beards_and_shavers_feature")
    FILEPATH = "features/beards_and_shavers_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        places_feature: Identifiable,
        bounding_box_min: list[int],
        bounding_box_max: list[int],
        y_delta: float,
        surface_block_type: BlockState,
        subsurface_block_type: BlockState,
        beard_raggedness_min: float,
        beard_raggedness_max: float,
    ):
        Feature.__init__(self, identifier)
        self.places_feature = places_feature
        self.bounding_box_min = bounding_box_min
        self.bounding_box_max = bounding_box_max
        self.y_delta = y_delta
        self.surface_block_type = surface_block_type
        self.subsurface_block_type = subsurface_block_type
        self.beard_raggedness_min = beard_raggedness_min
        self.beard_raggedness_max = beard_raggedness_max

    @property
    def surface_block_type(self) -> BlockState:
        return getattr(self, "_surface_block_type")

    @surface_block_type.setter
    def surface_block_type(self, value: BlockState):
        setattr(self, "_surface_block_type", BlockState.of(value))

    @property
    def subsurface_block_type(self) -> BlockState:
        return getattr(self, "_subsurface_block_type")

    @subsurface_block_type.setter
    def subsurface_block_type(self, value: BlockState):
        setattr(self, "_subsurface_block_type", BlockState.of(value))

    @property
    def beard_raggedness_min(self) -> float:
        return getattr(self, "_beard_raggedness_min")

    @beard_raggedness_min.setter
    def beard_raggedness_min(self, value: float):
        if not isinstance(value, float):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_beard_raggedness_min", value)

    @property
    def beard_raggedness_max(self) -> float:
        return getattr(self, "_beard_raggedness_max")

    @beard_raggedness_max.setter
    def beard_raggedness_max(self, value: float):
        if not isinstance(value, float):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_beard_raggedness_max", value)

    @property
    def places_feature(self) -> Identifier:
        return getattr(self, "_places_feature")

    @places_feature.setter
    def places_feature(self, value: Identifiable):
        setattr(self, "_places_feature", Identifiable.of(value))

    @property
    def bounding_box_min(self) -> Vector3:
        return getattr(self, "_bounding_box_min")

    @bounding_box_min.setter
    def bounding_box_min(self, value: Vector3):
        if not isinstance(value, Vector3):
            raise TypeError(
                f"Expected Vector3 but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_bounding_box_min", value)

    @property
    def bounding_box_max(self) -> Vector3:
        return getattr(self, "_bounding_box_max")

    @bounding_box_max.setter
    def bounding_box_max(self, value: Vector3):
        if not isinstance(value, Vector3):
            raise TypeError(
                f"Expected Vector3 but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_bounding_box_max", value)

    @property
    def y_delta(self) -> float:
        return getattr(self, "_y_delta")

    @y_delta.setter
    def y_delta(self, value: float):
        if not isinstance(value, float):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_y_delta", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = BeardsAndShaversFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["places_feature"] = str(self.places_feature)
        data[str(self.id)]["bounding_box_min"] = self.bounding_box_min.jsonify()
        data[str(self.id)]["bounding_box_max"] = self.bounding_box_max.jsonify()
        data[str(self.id)]["y_delta"] = self.y_delta
        data[str(self.id)]["surface_block_type"] = self.surface_block_type.jsonify()
        data[str(self.id)][
            "subsurface_block_type"
        ] = self.subsurface_block_type.jsonify()
        data[str(self.id)]["beard_raggedness_min"] = self.beard_raggedness_min
        data[str(self.id)]["beard_raggedness_max"] = self.beard_raggedness_max
        return data


class BeardsAndShaversFeatureLoader(Loader):
    name = "Beards and Shavers Feature"

    def __init__(self):
        from .schemas import BeardsAndShaversSchem1

        Loader.__init__(self, BeardsAndShaversFeature)
        self.add_schema(BeardsAndShaversSchem1, "1.13.0")
        self.add_schema(BeardsAndShaversSchem1, "1.16.0")


@feature_type
@behavior_pack
class CaveCarverFeature(Feature):
    """
    Represents a data-driven [Cave Carver Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Acave_carver_feature).
    """

    id = Identifier("cave_carver_feature")
    FILEPATH = "features/cave_carver_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        fill_with: BlockState,
        width_modifier: float,
        skip_carve_chance: int,
    ):
        Feature.__init__(self, identifier)
        self.fill_with = fill_with
        self.width_modifier = width_modifier
        self.skip_carve_chance = skip_carve_chance

    @property
    def width_modifier(self) -> float:
        return getattr(self, "_width_modifier")

    @width_modifier.setter
    def width_modifier(self, value: float):
        if not isinstance(value, float):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_width_modifier", value)

    @property
    def skip_carve_chance(self) -> int:
        return getattr(self, "_skip_carve_chance")

    @skip_carve_chance.setter
    def skip_carve_chance(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_skip_carve_chance", value)

    @property
    def fill_with(self) -> BlockState:
        return getattr(self, "_fill_with")

    @fill_with.setter
    def fill_with(self, value: BlockState):
        setattr(self, "_fill_with", BlockState.of(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = CaveCarverFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["fill_with"] = self.fill_with.jsonify()
        data[str(self.id)]["width_modifier"] = self.width_modifier
        data[str(self.id)]["skip_carve_chance"] = self.skip_carve_chance
        return data


class CaveCarverFeatureLoader(Loader):
    name = "Cave Carver Feature"

    def __init__(self):
        from .schemas import CaveCarverSchem1

        Loader.__init__(self, CaveCarverFeature)
        self.add_schema(CaveCarverSchem1, "1.13.0")
        self.add_schema(CaveCarverSchem1, "1.16.0")
        self.add_schema(CaveCarverSchem1, "1.16.100")


class ConditionalFeature:
    def __init__(self, places_feature: Identifiable, condition: Molang):
        self.places_feature = places_feature
        self.condition = condition

    @property
    def places_feature(self) -> Identifier:
        return getattr(self, "_places_feature")

    @places_feature.setter
    def places_feature(self, value: Identifiable):
        setattr(self, "_places_feature", Identifiable.of(value))

    @property
    def condition(self) -> Molang:
        return getattr(self, "_condition")

    @condition.setter
    def condition(self, value: Molang):
        if not isinstance(value, Molang):
            raise TypeError(
                f"Expected Molang but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_condition", value)

    def jsonify(self) -> dict:
        data = {
            "places_feature": str(self.places_feature),
            "condition": str(self.condition),
        }
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        places_feature = data.pop("places_feature")
        condition = Molang(data.pop("condition"))
        return ConditionalFeature(places_feature, condition)


@feature_type
@behavior_pack
class ConditionalListFeature(Feature):
    """
    Represents a data-driven [Conditional List Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Aconditional_list).
    """

    id = Identifier("conditional_list")
    FILEPATH = "features/conditional_list.json"

    def __init__(
        self,
        identifier: Identifiable,
        early_out_scheme: str = None,
        conditional_features: list[ConditionalFeature] = [],
    ):
        Feature.__init__(self, identifier)
        self.conditional_features = conditional_features
        self.early_out_scheme = early_out_scheme

    @property
    def conditional_features(self) -> list[ConditionalFeature]:
        return getattr(self, "_conditional_features")

    @conditional_features.setter
    def conditional_features(self, value: list[ConditionalFeature]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_conditional_features", value)

    @property
    def early_out_scheme(self) -> str:
        return getattr(self, "_early_out_scheme")

    @early_out_scheme.setter
    def early_out_scheme(self, value: str):
        if value is None:
            return
        setattr(self, "_early_out_scheme", str(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = ConditionalListLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["conditional_features"] = [
            x.jsonify() for x in self.conditional_features
        ]
        data[str(self.id)]["early_out_scheme"] = self.early_out_scheme
        return data

    def get_feature(self, index: int) -> ConditionalFeature:
        return self.conditional_features[index]

    def add_feature(self, feature: ConditionalFeature) -> ConditionalFeature:
        self.conditional_features.append(feature)
        return feature

    def remove_feature(self, index: int) -> ConditionalFeature:
        return self.conditional_features.pop(index)

    def clear_features(self) -> Self:
        self.conditional_features.clear()
        return self


class ConditionalListLoader(Loader):
    name = "Conditional List"

    def __init__(self):
        from .schemas import ConditionalListSchem1

        Loader.__init__(self, ConditionalListFeature)
        self.add_schema(ConditionalListSchem1, "1.13.0")
        self.add_schema(ConditionalListSchem1, "1.16.0")


@feature_type
@behavior_pack
class FossilFeature(Feature):
    """
    Represents a data-driven [Fossil Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Afossil_feature).
    """

    id = Identifier("fossil_feature")
    FILEPATH = "features/fossil_feature.json"

    def __init__(
        self, identifier: Identifiable, ore_block: BlockState, max_empty_corners: int
    ):
        Feature.__init__(self, identifier)
        self.ore_block = ore_block
        self.max_empty_corners = max_empty_corners

    @property
    def ore_block(self) -> BlockState:
        return getattr(self, "_ore_block")

    @ore_block.setter
    def ore_block(self, value: BlockState):
        setattr(self, "_ore_block", BlockState.of(value))

    @property
    def max_empty_corners(self) -> int:
        return getattr(self, "_max_empty_corners")

    @max_empty_corners.setter
    def max_empty_corners(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_max_empty_corners", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = FossilFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["ore_block"] = self.ore_block.jsonify()
        data[str(self.id)]["max_empty_corners"] = self.max_empty_corners
        return data


class FossilFeatureLoader(Loader):
    name = "Fossil Feature"

    def __init__(self):
        from .schemas import FossilSchem1

        Loader.__init__(self, FossilFeature)
        self.add_schema(FossilSchem1, "1.13.0")
        self.add_schema(FossilSchem1, "1.16.0")


# VV PROPS VV


@feature_type
@behavior_pack
class GeodeFeature(Feature):
    """
    Represents a data-driven [Geode Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Ageode_feature).
    """

    id = Identifier("geode_feature")
    FILEPATH = "features/geode_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        filler: BlockState,
        inner_layer: BlockState,
        alternate_inner_layer: BlockState,
        middle_layer: BlockState,
        outer_layer: BlockState,
        min_outer_wall_distance: int,
        max_outer_wall_distance: int,
        min_distribution_points: int,
        max_distribution_points: int,
        min_point_offset: int,
        max_point_offset: int,
        max_radius: int,
        crack_point_offset: int,
        generate_crack_chance: float,
        base_crack_size: float,
        noise_multiplier: float,
        use_potential_placements_chance: float,
        use_alternate_layer0_chance: float,
        placements_require_layer0_alternate: bool,
        invalid_blocks_threshold: int,
        inner_placements: list[BlockState] = [],
    ):
        Feature.__init__(self, identifier)
        self.filler = filler
        self.inner_layer = inner_layer
        self.alternate_inner_layer = alternate_inner_layer
        self.middle_layer = middle_layer
        self.outer_layer = outer_layer
        self.inner_placements = inner_placements
        self.min_outer_wall_distance = min_outer_wall_distance
        self.max_outer_wall_distance = max_outer_wall_distance
        self.min_distribution_points = min_distribution_points
        self.max_distribution_points = max_distribution_points
        self.min_point_offset = min_point_offset
        self.max_point_offset = max_point_offset
        self.max_radius = max_radius
        self.crack_point_offset = crack_point_offset
        self.generate_crack_chance = generate_crack_chance
        self.base_crack_size = base_crack_size
        self.noise_multiplier = noise_multiplier
        self.use_potential_placements_chance = use_potential_placements_chance
        self.use_alternate_layer0_chance = use_alternate_layer0_chance
        self.placements_require_layer0_alternate = placements_require_layer0_alternate
        self.invalid_blocks_threshold = invalid_blocks_threshold

    @property
    def inner_placements(self) -> list[BlockState]:
        return getattr(self, "_inner_placements")

    @inner_placements.setter
    def inner_placements(self, value: list[BlockState]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_inner_placements", [BlockState.of(x) for x in value])

    @property
    def outer_layer(self) -> BlockState:
        return getattr(self, "_outer_layer")

    @outer_layer.setter
    def outer_layer(self, value: BlockState):
        setattr(self, "_outer_layer", BlockState.of(value))

    @property
    def middle_layer(self) -> BlockState:
        return getattr(self, "_middle_layer")

    @middle_layer.setter
    def middle_layer(self, value: BlockState):
        setattr(self, "_middle_layer", BlockState.of(value))

    @property
    def alternate_inner_layer(self) -> BlockState:
        return getattr(self, "_alternate_inner_layer")

    @alternate_inner_layer.setter
    def alternate_inner_layer(self, value: BlockState):
        setattr(self, "_alternate_inner_layer", BlockState.of(value))

    @property
    def inner_layer(self) -> BlockState:
        return getattr(self, "_inner_layer")

    @inner_layer.setter
    def inner_layer(self, value: BlockState):
        setattr(self, "_inner_layer", BlockState.of(value))

    @property
    def filler(self) -> BlockState:
        return getattr(self, "_filler")

    @filler.setter
    def filler(self, value: BlockState):
        setattr(self, "_filler", BlockState.of(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = GeodeFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["filler"] = self.filler.jsonify()
        data[str(self.id)]["inner_layer"] = self.inner_layer.jsonify()
        data[str(self.id)][
            "alternate_inner_layer"
        ] = self.alternate_inner_layer.jsonify()
        data[str(self.id)]["middle_layer"] = self.middle_layer.jsonify()
        data[str(self.id)]["outer_layer"] = self.outer_layer.jsonify()
        data[str(self.id)]["inner_placements"] = [
            x.jsonify() for x in self.inner_placements
        ]
        data[str(self.id)]["min_outer_wall_distance"] = self.min_outer_wall_distance
        data[str(self.id)]["max_outer_wall_distance"] = self.max_outer_wall_distance
        data[str(self.id)]["min_distribution_points"] = self.min_distribution_points
        data[str(self.id)]["max_distribution_points"] = self.max_distribution_points
        data[str(self.id)]["min_point_offset"] = self.min_point_offset
        data[str(self.id)]["max_point_offset"] = self.max_point_offset
        data[str(self.id)]["max_radius"] = self.max_radius
        data[str(self.id)]["crack_point_offset"] = self.crack_point_offset
        data[str(self.id)]["generate_crack_chance"] = self.generate_crack_chance
        data[str(self.id)]["base_crack_size"] = self.base_crack_size
        data[str(self.id)]["noise_multiplier"] = self.noise_multiplier
        data[str(self.id)][
            "use_potential_placements_chance"
        ] = self.use_potential_placements_chance
        data[str(self.id)][
            "use_alternate_layer0_chance"
        ] = self.use_alternate_layer0_chance
        data[str(self.id)][
            "placements_require_layer0_alternate"
        ] = self.placements_require_layer0_alternate
        data[str(self.id)]["invalid_blocks_threshold"] = self.invalid_blocks_threshold
        return data

    # INNER PLACEMENTS
    def get_placement(self, index) -> BlockState:
        return self.inner_placements[index]

    def add_placement(self, inner_block: BlockState) -> BlockState:
        self.inner_placements.append(inner_block)
        return inner_block

    def remove_placement(self, index: int) -> BlockState:
        return self.inner_placements.pop(index)

    def clear_placements(self) -> Self:
        self.inner_placements.clear()
        return self


class GeodeFeatureLoader(Loader):
    name = "Geode Feature"

    def __init__(self):
        from .schemas import GeodeSchem1

        Loader.__init__(self, GeodeFeature)
        self.add_schema(GeodeSchem1, "1.13.0")
        self.add_schema(GeodeSchem1, "1.16.0")


@dataclass
class HeightDistribution:
    range: Range
    value: int

    @staticmethod
    def from_dict(data: dict) -> Self:
        return HeightDistribution(Range.from_dict(data[0], "range_"), data[1])

    def jsonify(self) -> dict:
        data = [self.range.jsonify("range_"), self.value]
        return data


class GrowingPlantBlock:

    def __init__(self, block: BlockState, value: int):
        self.block = block
        self.value = value

    @property
    def block(self) -> BlockState:
        return getattr(self, "_block")

    @block.setter
    def block(self, value: BlockState):
        setattr(self, "_block", BlockState.of(value))

    @property
    def value(self) -> int:
        return getattr(self, "_value")

    @value.setter
    def value(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_value", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        return GrowingPlantBlock(BlockState.from_dict(data[0]), data[1])

    def jsonify(self) -> dict:
        data = [self.block.jsonify(), self.value]
        return data


@feature_type
@behavior_pack
class GrowingPlantFeature(Feature):
    """
    Represents a data-driven [Growing Plant Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Agrowing_plant_feature).
    """

    id = Identifier("growing_plant_feature")
    FILEPATH = "features/growing_plant_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        growth_direction: str,
        allow_water: bool,
        age: Range = None,
        height_distribution: list[HeightDistribution] = [],
        body_blocks: list[GrowingPlantBlock] = [],
        head_blocks: list[GrowingPlantBlock] = [],
    ):
        Feature.__init__(self, identifier)
        self.height_distribution = height_distribution
        self.growth_direction = growth_direction
        self.age = age
        self.body_blocks = body_blocks
        self.head_blocks = head_blocks
        self.allow_water = allow_water

    @property
    def head_blocks(self) -> list[GrowingPlantBlock]:
        return getattr(self, "_head_blocks")

    @head_blocks.setter
    def head_blocks(self, value: list[GrowingPlantBlock]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_head_blocks", value)

    @property
    def body_blocks(self) -> list[GrowingPlantBlock]:
        return getattr(self, "_body_blocks")

    @body_blocks.setter
    def body_blocks(self, value: list[GrowingPlantBlock]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_body_blocks", value)

    @property
    def height_distribution(self) -> list[HeightDistribution]:
        return getattr(self, "_height_distribution")

    @height_distribution.setter
    def height_distribution(self, value: list[HeightDistribution]):
        if not isinstance(value, list):
            raise TypeError(f"Expected lt but got '{value.__class__.__name__}' instead")
        setattr(self, "_height_distribution", value)

    @property
    def allow_water(self) -> bool:
        return getattr(self, "_allow_water", False)

    @allow_water.setter
    def allow_water(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_allow_water", value)

    @property
    def growth_direction(self) -> str:
        return getattr(self, "_growth_direction")

    @growth_direction.setter
    def growth_direction(self, value: str):
        setattr(self, "_growth_direction", str(value))

    @property
    def age(self) -> Range:
        return getattr(self, "_age", None)

    @age.setter
    def age(self, value: Range):
        if value is None:
            return
        if not isinstance(value, Range):
            raise TypeError(
                f"Expected Range but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_age", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = GrowingPlantFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["height_distribution"] = [
            x.jsonify() for x in self.height_distribution
        ]
        data[str(self.id)]["growth_direction"] = self.growth_direction
        data[str(self.id)]["body_blocks"] = [x.jsonify() for x in self.body_blocks]
        data[str(self.id)]["head_blocks"] = [x.jsonify() for x in self.head_blocks]
        data[str(self.id)]["allow_water"] = self.allow_water
        if self.age is not None:
            data[str(self.id)]["age"] = self.age.jsonify("range_")
        return data

    # HEIGHT DISTRIBUTION

    def get_height_distribution(self, index: int) -> HeightDistribution:
        return self.height_distribution[index]

    def add_height_distribution(
        self, height_distribution: HeightDistribution
    ) -> HeightDistribution:
        self.height_distribution.append(height_distribution)
        return height_distribution

    def remove_height_distribution(self, index: int) -> HeightDistribution:
        return self.height_distribution.pop(index)

    def clear_height_distribution(self) -> Self:
        self.height_distribution.clear()
        return self

    # BODY BLOCKS

    def get_body_block(self, index: int) -> GrowingPlantBlock:
        return self.body_blocks[index]

    def add_body_block(self, block: GrowingPlantBlock) -> GrowingPlantBlock:
        self.body_blocks.append(block)
        return block

    def remove_body_block(self, index: int) -> GrowingPlantBlock:
        return self.body_blocks.pop(index)

    def clear_body_blocks(self) -> Self:
        self.body_blocks.clear()
        return self

    # HEAD BLOCKS

    def get_head_block(self, index: int) -> GrowingPlantBlock:
        return self.head_blocks[index]

    def add_head_block(self, block: GrowingPlantBlock) -> GrowingPlantBlock:
        self.head_blocks.append(block)
        return block

    def remove_head_block(self, index: int) -> GrowingPlantBlock:
        return self.head_blocks.pop(index)

    def clear_head_blocks(self) -> Self:
        self.head_blocks.clear()
        return self


class GrowingPlantFeatureLoader(Loader):
    name = "Growing Plant Feature"

    def __init__(self):
        from .schemas import GrowingPlantSchem1

        Loader.__init__(self, GrowingPlantFeature)
        self.add_schema(GrowingPlantSchem1, "1.13.0")
        self.add_schema(GrowingPlantSchem1, "1.16.0")


@feature_type
@behavior_pack
class NetherCaveCarverFeature(Feature):
    """
    Represents a data-driven [Nether Cave Carver Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Anether_cave_carver_feature).
    """

    id = Identifier("nether_cave_carver_feature")
    FILEPATH = "features/nether_cave_carver_feature.json"

    def __init__(
        self, identifier: Identifiable, fill_with: BlockState, width_modifier: float
    ):
        Feature.__init__(self, identifier)
        self.fill_with = fill_with
        self.width_modifier = width_modifier

    @property
    def fill_with(self) -> BlockState:
        return getattr(self, "_fill_with")

    @fill_with.setter
    def fill_with(self, value: BlockState):
        setattr(self, "_fill_with", BlockState.of(value))

    @property
    def width_modifier(self) -> float:
        return getattr(self, "_width_modifier")

    @width_modifier.setter
    def width_modifier(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_width_modifier", float(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = NetherCaveCarverFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["fill_with"] = self.fill_with.jsonify()
        data[str(self.id)]["width_modifier"] = self.width_modifier
        return data


class NetherCaveCarverFeatureLoader(Loader):
    name = "Nether Cave Carver Feature"

    def __init__(self):
        from .schemas import NetherCaveCarverSchem1

        Loader.__init__(self, NetherCaveCarverFeature)
        self.add_schema(NetherCaveCarverSchem1, "1.13.0")
        self.add_schema(NetherCaveCarverSchem1, "1.16.0")


@feature_type
@behavior_pack
class MultifaceFeature(Feature):
    """
    Represents a data-driven [Multiface Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Amultiface_feature).
    """

    id = Identifier("multiface_feature")
    FILEPATH = "features/multiface_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        places_block: BlockState,
        search_range: int,
        can_place_on_floor: bool,
        can_place_on_ceiling: bool,
        can_place_on_wall: bool,
        chance_of_spreading: float,
        can_place_on: list[BlockState] = [],
    ):
        Feature.__init__(self, identifier)
        self.places_block = places_block
        self.search_range = search_range
        self.can_place_on_floor = can_place_on_floor
        self.can_place_on_ceiling = can_place_on_ceiling
        self.can_place_on_wall = can_place_on_wall
        self.chance_of_spreading = chance_of_spreading
        self.can_place_on = can_place_on

    @property
    def places_block(self) -> BlockState:
        return getattr(self, "_places_block")

    @places_block.setter
    def places_block(self, value: BlockState):
        setattr(self, "_places_block", BlockState.of(value))

    @property
    def search_range(self) -> int:
        return getattr(self, "_search_range")

    @search_range.setter
    def search_range(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_search_range", value)

    @property
    def can_place_on_floor(self) -> bool:
        return getattr(self, "_can_place_on_floor")

    @can_place_on_floor.setter
    def can_place_on_floor(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_can_place_on_floor", value)

    @property
    def can_place_on_ceiling(self) -> bool:
        return getattr(self, "_can_place_on_ceiling")

    @can_place_on_ceiling.setter
    def can_place_on_ceiling(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_can_place_on_ceiling", value)

    @property
    def can_place_on_wall(self) -> bool:
        return getattr(self, "_can_place_on_wall")

    @can_place_on_wall.setter
    def can_place_on_wall(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_can_place_on_wall", value)

    @property
    def chance_of_spreading(self) -> float:
        return getattr(self, "_chance_of_spreading")

    @chance_of_spreading.setter
    def chance_of_spreading(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_chance_of_spreading", float(value))

    @property
    def can_place_on(self) -> list[BlockState]:
        return getattr(self, "_can_place_on")

    @can_place_on.setter
    def can_place_on(self, value: list[BlockState]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_can_place_on", [BlockState.of(x) for x in value])

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = MultifaceFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["places_block"] = self.places_block.jsonify()
        data[str(self.id)]["search_range"] = self.search_range
        data[str(self.id)]["can_place_on_floor"] = self.can_place_on_floor
        data[str(self.id)]["can_place_on_ceiling"] = self.can_place_on_ceiling
        data[str(self.id)]["can_place_on_wall"] = self.can_place_on_wall
        data[str(self.id)]["chance_of_spreading"] = self.chance_of_spreading
        data[str(self.id)]["can_place_on"] = [x.jsonify() for x in self.can_place_on]
        return data

    def get_place_on_block(self, index: int) -> BlockState:
        return self.can_place_on[index]

    def add_place_on_block(self, block: BlockState) -> BlockState:
        b = BlockState.of(block)
        self.can_place_on.append(b)
        return b

    def remove_place_on_block(self, index: int) -> BlockState:
        return self.can_place_on.pop(index)

    def clear_place_on_block(self) -> Self:
        self.can_place_on.clear()
        return self


class MultifaceFeatureLoader(Loader):
    name = "Multiface Feature"

    def __init__(self):
        from .schemas import MultifaceSchem1

        Loader.__init__(self, MultifaceFeature)
        self.add_schema(MultifaceSchem1, "1.13.0")
        self.add_schema(MultifaceSchem1, "1.16.0")


class ReplaceRule:
    def __init__(self, places_block: BlockState, may_replace: list[BlockState] = []):
        self.places_block = places_block
        self.may_replace = may_replace

    @property
    def places_block(self) -> BlockState:
        return getattr(self, "_places_block")

    @places_block.setter
    def places_block(self, value: BlockState):
        setattr(self, "_places_block", BlockState.of(value))

    @property
    def may_replace(self) -> list[BlockState]:
        return getattr(self, "_may_replace")

    @may_replace.setter
    def may_replace(self, value: list[BlockState]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_may_replace", [BlockState.of(x) for x in value])

    @staticmethod
    def from_dict(data: dict) -> Self:
        places_block = BlockState.from_dict(data.pop("places_block"))
        may_replace = [BlockState.from_dict(x) for x in data.pop("may_replace")]
        return ReplaceRule(places_block, may_replace)

    def jsonify(self) -> dict:
        data = {
            "places_block": self.places_block.jsonify(),
        }
        if self.may_replace:
            data["may_replace"] = [x.jsonify() for x in self.may_replace]
        return data

    def get_replace(self, index: int) -> BlockState:
        return self.may_replace[index]

    def add_replace(self, block: BlockState) -> BlockState:
        b = BlockState.of(block)
        self.may_replace.append(b)
        return b

    def remove_replace(self, index: int) -> BlockState:
        return self.may_replace.pop(index)

    def clear_replace(self) -> Self:
        self.may_replace.clear()
        return self


@feature_type
@behavior_pack
class OreFeature(Feature):
    """
    Represents a data-driven [Ore Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Aore_feature).
    """

    id = Identifier("ore_feature")
    FILEPATH = "features/ore_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        count: int,
        places_block: BlockState = None,
        replace_rules: list[ReplaceRule] = [],
    ):
        Feature.__init__(self, identifier)
        self.places_block = places_block
        self.count = count
        self.replace_rules = replace_rules

    @property
    def places_block(self) -> BlockState:
        return getattr(self, "_places_block", None)

    @places_block.setter
    def places_block(self, value: BlockState):
        if value is None:
            return
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_places_block", value)

    @property
    def count(self) -> int:
        return getattr(self, "_count")

    @count.setter
    def count(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_count", value)

    @property
    def replace_rules(self) -> list[ReplaceRule]:
        return getattr(self, "_replace_rules")

    @replace_rules.setter
    def replace_rules(self, value: list[ReplaceRule]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_replace_rules", value)

    def __iter__(self):
        for i in self.replace_rules:
            yield i

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = OreFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    # REPLACE RULE
    def get_rule(self, index: int) -> ReplaceRule:
        return self.replace_rules[index]

    def add_rule(self, rule: ReplaceRule) -> ReplaceRule:
        self.replace_rules.append(rule)
        return rule

    def remove_rule(self, index: int) -> ReplaceRule:
        return self.replace_rules.pop(index)

    def clear_rules(self) -> Self:
        self.replace_rules.clear()
        return self

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["count"] = self.count
        if self.places_block:
            data[str(self.id)]["places_block"] = self.places_block.jsonify()
        data[str(self.id)]["replace_rules"] = [x.jsonify() for x in self.replace_rules]
        return data


class OreFeatureLoader(Loader):
    name = "Ore Feature"

    def __init__(self):
        from .schemas import OreSchem1

        Loader.__init__(self, OreFeature)
        self.add_schema(OreSchem1, "1.13.0")
        self.add_schema(OreSchem1, "1.16.0")


@feature_type
@behavior_pack
class PartiallyExposedBlobFeature(Feature):
    """
    Represents a data-driven [Partially Exposed Blob Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Apartially_exposed_blob_feature).
    """

    id = Identifier("partially_exposed_blob_feature")
    FILEPATH = "features/partially_exposed_blob_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        places_block: BlockState,
        placement_radius_around_floor: int,
        placement_probability_per_valid_position: float,
        exposed_face: str,
    ):
        Feature.__init__(self, identifier)
        self.places_block = places_block
        self.placement_radius_around_floor = placement_radius_around_floor
        self.placement_probility_per_valid_position = (
            placement_probability_per_valid_position
        )
        self.exposed_face = exposed_face

    @property
    def places_block(self) -> BlockState:
        return getattr(self, "_places_block")

    @places_block.setter
    def places_block(self, value: BlockState):
        setattr(self, "_places_block", BlockState.of(value))

    @property
    def placement_radius_around_floor(self) -> int:
        return getattr(self, "_placement_radius_around_floor")

    @placement_radius_around_floor.setter
    def placement_radius_around_floor(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_placement_radius_around_floor", value)

    @property
    def placement_probility_per_valid_position(self) -> float:
        return getattr(self, "_placement_probility_per_valid_position")

    @placement_probility_per_valid_position.setter
    def placement_probility_per_valid_position(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_placement_probility_per_valid_position", float(value))

    @property
    def exposed_face(self) -> str:
        return getattr(self, "_exposed_face")

    @exposed_face.setter
    def exposed_face(self, value: str):
        setattr(self, "_exposed_face", str(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = PartiallyExposedBlobFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["places_block"] = self.places_block.jsonify()
        data[str(self.id)][
            "placement_radius_around_floor"
        ] = self.placement_radius_around_floor
        data[str(self.id)][
            "placement_probability_per_valid_position"
        ] = self.placement_probility_per_valid_position
        data[str(self.id)]["exposed_face"] = self.exposed_face
        return data


class PartiallyExposedBlobFeatureLoader(Loader):
    name = "Partially Exposed Blob Feature"

    def __init__(self):
        from .schemas import PartiallyExposedBlobSchem1

        Loader.__init__(self, PartiallyExposedBlobFeature)
        self.add_schema(PartiallyExposedBlobSchem1, "1.13.0")
        self.add_schema(PartiallyExposedBlobSchem1, "1.16.0")


class FeatureArea:
    def __init__(self, feature: Identifiable, area_dimentions: Vector2):
        self.feature = feature
        self.area_dimentions = area_dimentions

    @property
    def feature(self) -> Identifier:
        return getattr(self, "_feature")

    @feature.setter
    def feature(self, value: Identifiable):
        setattr(self, "_feature", Identifiable.of(value))

    @property
    def area_dimentions(self) -> Vector2:
        return getattr(self, "_area_dimentions")

    @area_dimentions.setter
    def area_dimentions(self, value: Vector2):
        if not isinstance(value, Vector2):
            raise TypeError(
                f"Expected Vector2 but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_area_dimentions", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        feature = data.pop("feature")
        area_dimentions = Vector2.from_dict(data.pop("area_dimentions"))
        return FeatureArea(feature, area_dimentions)

    def jsonify(self) -> dict:
        data = {
            "feature": str(self.feature),
            "area_dimentions": self.area_dimentions.jsonify(),
        }
        return data


@feature_type
@behavior_pack
class RectLayoutFeature(Feature):
    """
    Represents a data-driven [Rect Layout Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Arect_layout).
    """

    id = Identifier("rect_layout")
    FILEPATH = "features/rect_layout.json"

    def __init__(
        self,
        identifier: Identifiable,
        ratio_of_empty_space: float,
        feature_areas: list[FeatureArea] = [],
    ):
        Feature.__init__(self, identifier)
        self.ratio_of_empty_space = ratio_of_empty_space
        self.feature_areas = feature_areas

    @property
    def ratio_of_empty_space(self) -> float:
        return getattr(self, "_ratio_of_empty_space")

    @ratio_of_empty_space.setter
    def ratio_of_empty_space(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_ratio_of_empty_space", float(value))

    @property
    def feature_areas(self) -> list[FeatureArea]:
        return getattr(self, "_feature_areas")

    @feature_areas.setter
    def feature_areas(self, value: list[FeatureArea]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_feature_areas", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = RectLayoutFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["ratio_of_empty_space"] = self.ratio_of_empty_space
        data[str(self.id)]["feature_areas"] = [x.jsonify() for x in self.feature_areas]
        return data

    # FEATURE AREA

    def get_feature_area(self, index: int) -> FeatureArea:
        return self.feature_areas[index]

    def add_feature_area(self, feature_area: FeatureArea) -> FeatureArea:
        self.feature_areas.append(feature_area)
        return feature_area

    def remove_feature_area(self, index: int) -> FeatureArea:
        return self.feature_areas.pop(index)

    def clear_feature_areas(self) -> Self:
        self.feature_areas.clear()
        return self


class RectLayoutFeatureLoader(Loader):
    name = "Rect Layout"

    def __init__(self):
        from .schemas import RectLayoutSchem1

        Loader.__init__(self, RectLayoutFeature)
        self.add_schema(RectLayoutSchem1, "1.13.0")
        self.add_schema(RectLayoutSchem1, "1.16.0")


@feature_type
@behavior_pack
class ScanSurfaceFeature(Feature):
    """
    Represents a data-driven [Scan Surface Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Ascan_surface).
    """

    id = Identifier("scan_surface")
    FILEPATH = "features/scan_surface.json"

    def __init__(self, identifier: Identifiable, scan_surface_feature: Identifiable):
        Feature.__init__(self, identifier)
        self.scan_surface_feature = scan_surface_feature

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = ScanSurfaceFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["scan_surface_feature"] = str(self.scan_surface_feature)
        return data


class ScanSurfaceFeatureLoader(Loader):
    name = "Scan Surface"

    def __init__(self):
        from .schemas import ScanSurfaceSchem1

        Loader.__init__(self, ScanSurfaceFeature)
        self.add_schema(ScanSurfaceSchem1, "1.13.0")
        self.add_schema(ScanSurfaceSchem1, "1.16.0")


class DistributionProvider:
    def __init__(
        self,
        distribution: str,
        extent: Vector2,
        step_size: int = None,
        grid_offset: int = None,
    ):
        self.distribution = distribution
        self.extent = extent
        self.step_size = step_size
        self.grid_offset = grid_offset

    @property
    def step_size(self) -> int:
        return getattr(self, "_step_size", None)

    @step_size.setter
    def step_size(self, value: int):
        if value is None:
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_step_size", value)

    @property
    def grid_offset(self) -> int:
        return getattr(self, "_grid_offset", None)

    @grid_offset.setter
    def grid_offset(self, value: int):
        if value is None:
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_grid_offset", value)

    @property
    def distribution(self) -> str:
        return getattr(self, "_distribution")

    @distribution.setter
    def distribution(self, value: str):
        setattr(self, "_distribution", str(value))

    @property
    def extent(self) -> Vector2:
        return getattr(self, "_extent")

    @extent.setter
    def extent(self, value: Vector2):
        if not isinstance(value, Vector2):
            raise TypeError(
                f"Expected Vector2 but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_extent", value)

    @staticmethod
    def from_dict(data: dict) -> Self | int:
        if isinstance(data, int):
            return data
        distribution = data.pop("distribution")
        extent = Vector2(*data.pop("extent"))
        return DistributionProvider(distribution, extent)

    def jsonify(self) -> dict:
        data = {"distribution": self.distribution, "extent": self.extent.jsonify()}
        if self.step_size:
            data["step_size"] = self.step_size
        if self.grid_offset:
            data["grid_offset"] = self.grid_offset
        return data


@feature_type
@behavior_pack
class ScatterFeature(Feature):
    """
    Represents a data-driven [Scatter Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Ascatter_feature).
    """

    id = Identifier("scatter_feature")
    FILEPATH = "features/scatter_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        places_feature: Identifiable,
        iterations: Molang,
        x: DistributionProvider | int,
        y: DistributionProvider | int,
        z: DistributionProvider | int,
        scatter_chance: float = None,
    ):
        Feature.__init__(self, identifier)
        self.places_feature = places_feature
        self.iterations = iterations
        self.scatter_chance = scatter_chance
        self.x = x
        self.y = y
        self.z = z

    @property
    def z(self) -> DistributionProvider | int:
        return getattr(self, "_z")

    @z.setter
    def z(self, value: DistributionProvider | int):
        if not isinstance(value, (DistributionProvider, int)):
            raise TypeError(
                f"Expected Distribution, int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_z", value)

    @property
    def y(self) -> DistributionProvider | int:
        return getattr(self, "_y")

    @y.setter
    def y(self, value: DistributionProvider | int):
        if not isinstance(value, (DistributionProvider, int)):
            raise TypeError(
                f"Expected Distribution, int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_y", value)

    @property
    def x(self) -> DistributionProvider | int:
        return getattr(self, "_x")

    @x.setter
    def x(self, value: DistributionProvider | int):
        if not isinstance(value, (DistributionProvider, int)):
            raise TypeError(
                f"Expected Distribution, int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_x", value)

    @property
    def scatter_chance(self) -> float:
        return getattr(self, "_scatter_chance", None)

    @scatter_chance.setter
    def scatter_chance(self, value: float):
        if value is None:
            return
        if not isinstance(value, float):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_scatter_chance", value)

    @property
    def iterations(self) -> int:
        return getattr(self, "_iterations")

    @iterations.setter
    def iterations(self, value: Molang):
        if not isinstance(value, (Molang, int)):
            raise TypeError(
                f"Expected Molang, int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_iterations", Molang(value))

    @property
    def places_feature(self) -> Identifier:
        return getattr(self, "_places_feature")

    @places_feature.setter
    def places_feature(self, value: Identifiable):
        setattr(self, "_places_feature", Identifiable.of(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = ScatterFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["places_feature"] = str(self.places_feature)
        data[str(self.id)]["iterations"] = self.iterations
        if self.scatter_chance:
            data[str(self.id)]["scatter_chance"] = self.scatter_chance
        data[str(self.id)]["x"] = (
            self.x.jsonify() if isinstance(self.x, DistributionProvider) else self.x
        )
        data[str(self.id)]["y"] = (
            self.y.jsonify() if isinstance(self.y, DistributionProvider) else self.y
        )
        data[str(self.id)]["z"] = (
            self.z.jsonify() if isinstance(self.z, DistributionProvider) else self.z
        )
        return data


class ScatterFeatureLoader(Loader):
    name = "Scatter Feature"

    def __init__(self):
        from .schemas import ScatterSchem1

        Loader.__init__(self, ScatterFeature)
        self.add_schema(ScatterSchem1, "1.13.0")
        self.add_schema(ScatterSchem1, "1.16.0")


@feature_type
@behavior_pack
class SculkPatchFeature(Feature):
    """
    Represents a data-driven [Sculk Patch Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Asculk_patch_feature).
    """

    id = Identifier("sculk_patch_feature")
    FILEPATH = "features/sculk_patch_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        central_block: BlockState,
        central_block_placement_chance: float,
        charge_amount: int,
        cursor_count: int,
        growth_rounds: int,
        spread_attempts: int,
        spread_rounds: int,
        extra_growth_chance: Range,
        can_place_sculk_patch_on: list[BlockState] = [],
    ):
        Feature.__init__(self, identifier)
        self.can_place_sculk_patch_on = can_place_sculk_patch_on
        self.central_block = central_block
        self.central_block_placement_chance = central_block_placement_chance
        self.charge_amount = charge_amount
        self.cursor_count = cursor_count
        self.growth_rounds = growth_rounds
        self.spread_attempts = spread_attempts
        self.spread_rounds = spread_rounds
        self.extra_growth_chance = extra_growth_chance

    @property
    def central_block(self) -> BlockState:
        return getattr(self, "_central_block")

    @central_block.setter
    def central_block(self, value: BlockState):
        setattr(self, "_central_block", BlockState.of(value))

    @property
    def central_block_placement_chance(self) -> float:
        return getattr(self, "_central_block_placement_chance")

    @central_block_placement_chance.setter
    def central_block_placement_chance(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_central_block_placement_chance", float(value))

    @property
    def charge_amount(self) -> int:
        return getattr(self, "_charge_amount")

    @charge_amount.setter
    def charge_amount(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_charge_amount", value)

    @property
    def growth_rounds(self) -> int:
        return getattr(self, "_growth_rounds")

    @growth_rounds.setter
    def growth_rounds(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_growth_rounds", value)

    @property
    def spread_attempts(self) -> int:
        return getattr(self, "_spread_attempts")

    @spread_attempts.setter
    def spread_attempts(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_spread_attempts", value)

    @property
    def spread_rounds(self) -> int:
        return getattr(self, "_spread_rounds")

    @spread_rounds.setter
    def spread_rounds(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_spread_rounds", value)

    @property
    def extra_growth_chance(self) -> Range:
        return getattr(self, "_extra_growth_chance", None)

    @extra_growth_chance.setter
    def extra_growth_chance(self, value: Range):
        if not isinstance(value, Range):
            raise TypeError(
                f"Expected Range but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_extra_growth_chance", value)

    @property
    def can_place_sculk_patch_on(self) -> list[BlockState]:
        return getattr(self, "_can_place_sculk_patch_on")

    @can_place_sculk_patch_on.setter
    def can_place_sculk_patch_on(self, value: list[BlockState]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_can_place_sculk_patch_on", [BlockState.of(x) for x in value])

    @property
    def cursor_count(self) -> int:
        return getattr(self, "_cursor_count")

    @cursor_count.setter
    def cursor_count(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_cursor_count", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = SculkPatchFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["can_place_sculk_patch_on"] = [
            x.jsonify() for x in self.can_place_sculk_patch_on
        ]
        data[str(self.id)]["central_block"] = self.central_block.jsonify()
        data[str(self.id)][
            "central_block_placement_chance"
        ] = self.central_block_placement_chance
        data[str(self.id)]["charge_amount"] = self.charge_amount
        data[str(self.id)]["cursor_count"] = self.cursor_count
        data[str(self.id)]["growth_rounds"] = self.growth_rounds
        data[str(self.id)]["spread_attempts"] = self.spread_attempts
        data[str(self.id)]["spread_rounds"] = self.spread_rounds
        if self.extra_growth_chance is not None:
            data[str(self.id)]["extra_growth_chance"] = (
                self.extra_growth_chance.jsonify("range_")
            )
        return data

    # CAN PLACE ON

    def get_can_place_on(self, index: int) -> BlockState:
        return self.can_place_sculk_patch_on[index]

    def add_can_place_on(self, block: BlockState) -> BlockState:
        b = BlockState.of(block)
        self.can_place_sculk_patch_on.append(b)
        return b

    def remove_can_place_on(self, index: int) -> BlockState:
        return self.can_place_sculk_patch_on.pop(index)

    def clear_can_place_on(self) -> Self:
        self.can_place_sculk_patch_on.clear()
        return self


class SculkPatchFeatureLoader(Loader):
    name = "Sculk Patch Feature"

    def __init__(self):
        from .schemas import SculkPatchSchem1

        Loader.__init__(self, SculkPatchFeature)
        self.add_schema(SculkPatchSchem1, "1.13.0")
        self.add_schema(SculkPatchSchem1, "1.16.0")


@feature_type
@behavior_pack
class SearchFeature(Feature):
    """
    Represents a data-driven [Search Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Asearch_feature).
    """

    id = Identifier("search_feature")
    FILEPATH = "features/search_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        places_feature: Identifiable,
        search_volume: VectorRange,
        search_axis: str,
        required_successes: int,
    ):
        Feature.__init__(self, identifier)
        self.places_feature = places_feature
        self.search_volume = search_volume
        self.search_axis = search_axis
        self.required_successes = required_successes

    @property
    def places_feature(self) -> Identifier:
        return getattr(self, "_places_feature")

    @places_feature.setter
    def places_feature(self, value: Identifiable):
        setattr(self, "_places_feature", Identifiable.of(value))

    @property
    def search_volume(self) -> VectorRange:
        return getattr(self, "_search_volume")

    @search_volume.setter
    def search_volume(self, value: VectorRange):
        if not isinstance(value, VectorRange):
            raise TypeError(
                f"Expected VectorRange but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_search_volume", value)

    @property
    def search_axis(self) -> str:
        return getattr(self, "_search_axis")

    @search_axis.setter
    def search_axis(self, value: str):
        setattr(self, "_search_axis", str(value))

    @property
    def required_successes(self) -> int:
        return getattr(self, "_required_successes")

    @required_successes.setter
    def required_successes(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_required_successes", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = SearchFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["places_feature"] = str(self.places_feature)
        data[str(self.id)]["search_volume"] = self.search_volume.jsonify()
        data[str(self.id)]["search_axis"] = self.search_axis
        data[str(self.id)]["required_successes"] = self.required_successes
        return data


class SearchFeatureLoader(Loader):
    name = "Search Feature"

    def __init__(self):
        from .schemas import SearchSchem1

        Loader.__init__(self, SearchFeature)
        self.add_schema(SearchSchem1, "1.13.0")
        self.add_schema(SearchSchem1, "1.16.0")


@feature_type
@behavior_pack
class SingleBlockFeature(Feature):
    """
    Represents a data-driven [Single Block Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Asingle_block_feature).
    """

    id = Identifier("single_block_feature")
    FILEPATH = "features/single_block_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        places_block: BlockState,
        enforce_placement_rule: bool,
        enforce_survivability_rule: bool = False,
        may_place_on: list[BlockState] = [],
        may_replace: list[BlockState] = [],
    ):
        Feature.__init__(self, identifier)
        self.places_block = places_block
        self.enforce_placement_rule = enforce_placement_rule
        self.enforce_survivability_rule = enforce_survivability_rule
        self.may_place_on = may_place_on
        self.may_replace = may_replace

    @property
    def places_block(self) -> BlockState:
        return getattr(self, "_places_block")

    @places_block.setter
    def places_block(self, value: BlockState):
        setattr(self, "_places_block", BlockState.of(value))

    @property
    def enforce_placement_rule(self) -> bool:
        return getattr(self, "_enforce_placement_rule", False)

    @enforce_placement_rule.setter
    def enforce_placement_rule(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_enforce_placement_rule", value)

    @property
    def enforce_survivability_rule(self) -> bool:
        return getattr(self, "_enforce_survivability_rule", False)

    @enforce_survivability_rule.setter
    def enforce_survivability_rule(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_enforce_survivability_rule", value)

    @property
    def may_place_on(self) -> list[BlockState]:
        return getattr2(self, "_may_place_on", [])

    @may_place_on.setter
    def may_place_on(self, value: list[BlockState]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_may_place_on", [BlockState.of(x) for x in value])

    @property
    def may_replace(self) -> list[BlockState]:
        return getattr2(self, "_may_replace", [])

    @may_replace.setter
    def may_replace(self, value: list[BlockState]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_may_replace", [BlockState.of(x) for x in value])

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = SingleBlockFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["places_block"] = self.places_block.jsonify()
        data[str(self.id)]["enforce_placement_rule"] = self.enforce_placement_rule
        if self.enforce_survivability_rule:
            data[str(self.id)][
                "enforce_survivability_rule"
            ] = self.enforce_survivability_rule
        if self.may_place_on:
            data[str(self.id)]["may_place_on"] = [
                x.jsonify() for x in self.may_place_on
            ]
        if self.may_replace:
            data[str(self.id)]["may_replace"] = [x.jsonify() for x in self.may_replace]
        return data

    # PLACE ON

    def get_place_on(self, index: int) -> BlockState:
        return self.may_place_on[index]

    def add_place_on(self, block: BlockState) -> BlockState:
        b = BlockState.of(block)
        self.may_place_on.append(b)
        return b

    def remove_place_on(self, index: int) -> BlockState:
        return self.may_place_on.pop(index)

    def clear_place_on(self) -> Self:
        self.may_place_on.clear()
        return self

    # REPLACE

    def get_replace(self, index: int) -> BlockState:
        return self.may_replace[index]

    def add_replace(self, block: BlockState) -> BlockState:
        b = BlockState.of(block)
        self.may_replace.append(b)
        return b

    def remove_replace(self, index: int) -> BlockState:
        return self.may_replace.pop(index)

    def claer_replace(self) -> Self:
        self.may_replace.clear()
        return self


class SingleBlockFeatureLoader(Loader):
    name = "Single Block Feature"

    def __init__(self):
        from .schemas import SingleBlockSchem1

        Loader.__init__(self, SingleBlockFeature)
        self.add_schema(SingleBlockSchem1, "1.13.0")
        self.add_schema(SingleBlockSchem1, "1.16.0")


@feature_type
@behavior_pack
class SnapToSurfaceFeature(Feature):
    """
    Represents a data-driven [Snap To Surface Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Asnap_to_surface_feature).
    """

    id = Identifier("snap_to_surface_feature")
    FILEPATH = "features/snap_to_surface_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        feature_to_snap: Identifiable,
        vertical_search_range: int,
        surface: str,
    ):
        Feature.__init__(self, identifier)
        self.feature_to_snap = feature_to_snap
        self.vertical_search_range = vertical_search_range
        self.surface = surface

    @property
    def feature_to_snap(self) -> Identifier:
        return getattr(self, "_feature_to_snap")

    @feature_to_snap.setter
    def feature_to_snap(self, value: Identifiable):
        setattr(self, "_feature_to_snap", Identifiable.of(value))

    @property
    def vertical_search_range(self) -> int:
        return getattr(self, "_vertical_search_range")

    @vertical_search_range.setter
    def vertical_search_range(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_vertical_search_range", value)

    @property
    def surface(self) -> str:
        return getattr(self, "_surface")

    @surface.setter
    def surface(self, value: str):
        setattr(self, "_surface", str(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = SnapToSurfaceFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["feature_to_snap"] = str(self.feature_to_snap)
        data[str(self.id)]["vertical_search_range"] = self.vertical_search_range
        data[str(self.id)]["surface"] = self.surface
        return data


class SnapToSurfaceFeatureLoader(Loader):
    name = "Snap To Surface Feature"

    def __init__(self):
        from .schemas import SnapToSurfaceSchem1

        Loader.__init__(self, SnapToSurfaceFeature)
        self.add_schema(SnapToSurfaceSchem1, "1.13.0")
        self.add_schema(SnapToSurfaceSchem1, "1.16.0")


class BlockIntersection:
    def __init__(
        self,
        block_allowlist: list[BlockState] = [],
        block_denylist: list[BlockState] = [],
    ):
        self.block_allowlist = block_allowlist
        self.block_denylist = block_denylist

    @property
    def block_allowlist(self) -> list[BlockState]:
        return getattr2(self, "_block_allowlist", [])

    @block_allowlist.setter
    def block_allowlist(self, value: list[BlockState]):
        if value is None:
            value = []
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_block_allowlist", [BlockState.of(x) for x in value])

    @property
    def block_denylist(self) -> list[BlockState]:
        return getattr2(self, "_block_denylist", [])

    @block_denylist.setter
    def block_denylist(self, value: list[BlockState]):
        if value is None:
            value = []
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_block_denylist", [BlockState.of(x) for x in value])

    @staticmethod
    def from_dict(data: dict) -> Self:
        block_allowlist = (
            data.pop("block_allowlist") if "block_allowlist" in data else None
        )
        block_denylist = (
            data.pop("block_denylist") if "block_denylist" in data else None
        )
        return BlockIntersection(block_allowlist, block_denylist)

    def jsonify(self) -> dict:
        data = {}
        if self.block_allowlist:
            data["block_allowlist"] = [x.jsonify() for x in self.block_allowlist]
        if self.block_denylist:
            data["block_denylist"] = [x.jsonify() for x in self.block_denylist]
        return data

    # ALLOWLIST

    def get_allow_block(self, index: int) -> BlockState:
        return self.block_allowlist[index]

    def add_allow_block(self, block: BlockState) -> BlockState:
        b = BlockState.of(block)
        self.block_allowlist.append(b)
        return b

    def remove_allow_block(self, index: int) -> BlockState:
        return self.block_allowlist.pop(index)

    def clear_allow_blocks(self) -> Self:
        self.block_allowlist.clear()
        return self

    # DENYLIST

    def get_deny_block(self, index: int) -> BlockState:
        return self.block_denylist[index]

    def add_deny_block(self, block: BlockState) -> BlockState:
        b = BlockState.of(block)
        self.block_denylist.append(b)
        return b

    def remove_deny_block(self, index: int) -> BlockState:
        return self.block_denylist.pop(index)

    def clear_deny_blocks(self) -> Self:
        self.block_denylist.clear()
        return self


class Constraints:
    def __init__(self, unburied: bool, block_intersection: BlockIntersection):
        self.unburied = unburied
        self.block_intersection = block_intersection

    @staticmethod
    def from_dict(data: dict) -> Self:
        unburied = False
        if "unburied" in data:
            unburied = True
        block_intersection = BlockIntersection.from_dict(data.pop("block_intersection"))
        return Constraints(unburied, block_intersection)

    def jsonify(self) -> dict:
        data = {"block_intersection": self.block_intersection.jsonify()}
        if self.unburied:
            data["unburied"] = {}
        return data


@feature_type
@behavior_pack
class StructureTemplateFeature(Feature):
    """
    Represents a data-driven [Structure Template Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Astructure_template_feature).
    """

    id = Identifier("structure_template_feature")
    FILEPATH = "features/structure_template_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        structure_name: Identifiable,
        adjustment_radius: int,
        facing_direction: str,
        constraints: Constraints,
    ):
        Feature.__init__(self, identifier)
        self.structure_name = structure_name
        self.adjustment_radius = adjustment_radius
        self.facing_direction = facing_direction
        self.constraints = constraints

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = StructureTemplateFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["structure_name"] = str(self.structure_name)
        data[str(self.id)]["adjustment_radius"] = self.adjustment_radius
        data[str(self.id)]["facing_direction"] = self.facing_direction
        data[str(self.id)]["constraints"] = self.constraints.jsonify()
        return data


class StructureTemplateFeatureLoader(Loader):
    name = "Structure Template Feature"

    def __init__(self):
        from .schemas import StructureTemplateSchem1

        Loader.__init__(self, StructureTemplateFeature)
        self.add_schema(StructureTemplateSchem1, "1.13.0")
        self.add_schema(StructureTemplateSchem1, "1.16.0")


@feature_type
@behavior_pack
class SurfaceRelativeThresholdFeature(Feature):
    """
    Represents a data-driven [Surface Relative Threshold Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Asurface_relative_threshold_feature).
    """

    id = Identifier("surface_relative_threshold_feature")
    FILEPATH = "features/surface_relative_threshold_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        feature_to_snap: Identifiable,
        minimum_distance_below_surface: int,
    ):
        Feature.__init__(self, identifier)
        self.feature_to_snap = feature_to_snap
        self.minimum_distance_below_surface = minimum_distance_below_surface

    @property
    def feature_to_snap(self) -> Identifier:
        return getattr(self, "_feature_to_snap", None)

    @feature_to_snap.setter
    def feature_to_snap(self, value: Identifiable):
        setattr(self, "_feature_to_snap", Identifiable.of(value))

    @property
    def minimum_distance_below_surface(self) -> int:
        return getattr(self, "_minimum_distance_below_surface")

    @minimum_distance_below_surface.setter
    def minimum_distance_below_surface(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_minimum_distance_below_surface", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = SurfaceRelativeThresholdFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        if self.feature_to_snap:
            data[str(self.id)]["feature_to_snap"] = str(self.feature_to_snap)
        data[str(self.id)][
            "minimum_distance_below_surface"
        ] = self.minimum_distance_below_surface
        return data


class SurfaceRelativeThresholdFeatureLoader(Loader):
    name = "Surface Relative Threshold Feature"

    def __init__(self):
        from .schemas import SurfaceRelativeThresholdSchem1

        Loader.__init__(self, SurfaceRelativeThresholdFeature)
        self.add_schema(SurfaceRelativeThresholdSchem1, "1.13.0")
        self.add_schema(SurfaceRelativeThresholdSchem1, "1.16.0")


@feature_type
@behavior_pack
class UnderwaterCaveCarverFeature(Feature):
    """
    Represents a data-driven [Underwater Cave Carver Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Aunderwater_cave_carver_feature).
    """

    id = Identifier("underwater_cave_carver_feature")
    FILEPATH = "features/underwater_cave_carver_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        fill_with: BlockState,
        width_modifier: float,
        replace_air_with: BlockState,
    ):
        Feature.__init__(self, identifier)
        self.fill_with = fill_with
        self.width_modifier = width_modifier
        self.replace_air_with = replace_air_with

    @property
    def fill_with(self) -> BlockState:
        return getattr(self, "_fill_with")

    @fill_with.setter
    def fill_with(self, value: BlockState):
        setattr(self, "_fill_with", BlockState.of(value))

    @property
    def width_modifier(self) -> float:
        return getattr(self, "_width_modifier")

    @width_modifier.setter
    def width_modifier(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_width_modifier", float(value))

    @property
    def replace_air_with(self) -> BlockState:
        return getattr(self, "_replace_air_with")

    @replace_air_with.setter
    def replace_air_with(self, value: BlockState):
        setattr(self, "_replace_air_with", BlockState.of(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = UnderwaterCaveCarverFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["fill_with"] = self.fill_with.jsonify()
        data[str(self.id)]["width_modifier"] = self.width_modifier
        data[str(self.id)]["replace_air_with"] = self.replace_air_with.jsonify()
        return data


class UnderwaterCaveCarverFeatureLoader(Loader):
    name = "Underwater Cave Carver Feature"

    def __init__(self):
        from .schemas import UnderwaterCaveCarverSchem1

        Loader.__init__(self, UnderwaterCaveCarverFeature)
        self.add_schema(UnderwaterCaveCarverSchem1, "1.13.0")
        self.add_schema(UnderwaterCaveCarverSchem1, "1.16.0")


class Cluster:
    def __init__(
        self, may_replace: list[BlockState], num_clusters: int, cluster_radius: int
    ):
        self.may_replace = may_replace
        self.num_clusters = num_clusters
        self.cluster_radius = cluster_radius

    @property
    def may_replace(self) -> list[BlockState]:
        return getattr(self, "_may_replace")

    @may_replace.setter
    def may_replace(self, value: list[BlockState]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_may_replace", [BlockState.of(x) for x in value])

    @property
    def num_clusters(self) -> int:
        return getattr(self, "_num_clusters")

    @num_clusters.setter
    def num_clusters(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_num_clusters", value)

    @property
    def cluster_radius(self) -> int:
        return getattr(self, "_cluster_radius")

    @cluster_radius.setter
    def cluster_radius(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_cluster_radius", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        may_replace = [BlockState.of(x) for x in data.pop("may_replace")]
        num_clusters = data.pop("num_clusters")
        cluster_radius = data.pop("cluster_radius")
        return Cluster(may_replace, num_clusters, cluster_radius)

    def jsonify(self) -> dict:
        data = {
            "may_replace": [x.jsonify() for x in self.may_replace],
            "num_clusters": self.num_clusters,
            "cluster_radius": self.cluster_radius,
        }
        return data


class TrunkHeight:
    def __init__(
        self, base: int, intervals: list[int], min_height_for_canopy: int = None
    ):
        self.base = base
        self.intervals = intervals
        self.min_height_for_canopy = min_height_for_canopy

    @property
    def base(self) -> int:
        return getattr(self, "_base")

    @base.setter
    def base(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_base", value)

    @property
    def intervals(self) -> list[int]:
        return getattr(self, "_intervals")

    @intervals.setter
    def intervals(self, value: list[int]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_intervals", value)

    @property
    def num_height_for_canopy(self) -> int:
        return getattr(self, "_num_height_for_canopy")

    @num_height_for_canopy.setter
    def num_height_for_canopy(self, value: int):
        if value is None:
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_num_height_for_canopy", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        return TrunkHeight(**data)

    def jsonify(self) -> dict:
        data = {
            "base": self.base,
            "intervals": self.intervals,
            "min_height_for_canopy": self.min_height_for_canopy,
        }
        return data


@dataclass
class FancyHeight:
    base: int
    variance: int
    scale: float

    @staticmethod
    def from_dict(data: dict) -> Self:
        return FancyHeight(**data)

    def jsonify(self) -> dict:
        data = {"base": self.base, "variance": self.variance, "scale": self.scale}
        return data


@dataclass
class MangroveHeight:
    base: int
    height_rand_a: int
    height_rand_b: int
    variance: int = None
    scale: float = 1.0

    @staticmethod
    def from_dict(data: dict) -> Self:
        return MangroveHeight(**data)

    def jsonify(self) -> dict:
        data = {
            "base": self.base,
            "height_rand_a": self.height_rand_a,
            "height_rand_b": self.height_rand_b,
        }
        if self.variance:
            data["variance"] = self.variance
        if self.scale:
            data["scale"] = self.scale
        return data


@dataclass
class TrunkLean:
    allow_diagonal_growth: bool
    lean_height: Range
    lean_steps: Range
    lean_length: Range = None

    @staticmethod
    def from_dict(data: dict) -> Self:
        allow_diagonal_growth = data.pop("allow_diagonal_growth")
        lean_height = Range.from_dict(data.pop("lean_height"), "range_")
        lean_steps = Range.from_dict(data.pop("lean_steps"), "range_")
        lean_length = (
            Range.from_dict(data.pop("lean_length"), "range_")
            if "lean_length" in data
            else None
        )
        return TrunkLean(allow_diagonal_growth, lean_height, lean_steps, lean_length)

    def jsonify(self) -> dict:
        data = {
            "allow_diagonal_growth": self.allow_diagonal_growth,
            "lean_height": self.lean_height.jsonify("range_"),
            "lean_steps": self.lean_steps.jsonify("range_"),
        }
        if self.lean_length is not None:
            data["lean_length"] = self.lean_length.jsonify("range_")
        return data


class CanopyType:
    @property
    def id(self) -> Identifier:
        return getattr(self, "_id", Identifier("canopy_type"))

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier.of(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        for id in data.keys():
            clazz = INSTANCE.get_registry(Registries.TREE_CANOPY).get(id)
            if clazz is not None:
                return clazz.from_dict(data[id])


@dataclass
class Branches:
    branch_length: int
    branch_chance: float
    branch_steps: int = None
    branch_position: int = None

    @staticmethod
    def from_dict(data: dict) -> Self:
        return Branches(**data)

    def jsonify(self) -> dict:
        data = {
            "branch_length": self.branch_length,
            "branch_chance": self.branch_chance,
        }
        if self.branch_steps:
            data["branch_steps"] = self.branch_steps
        if self.branch_position:
            data["branch_position"] = self.branch_position
        return data


@dataclass
class AcaciaBranches(Branches):
    branch_canopy: CanopyType = None

    @staticmethod
    def from_dict(data: dict) -> Self:
        branch_canopy = CanopyType.from_dict(data.pop("branch_canopy"))
        return AcaciaBranches(**data, branch_canopy=branch_canopy)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["branch_canopy"] = self.branch_canopy.jsonify()
        return data


@dataclass
class MegaBranches:
    branch_length: int
    branch_slope: float
    branch_interval: int
    branch_canopy: CanopyType

    @staticmethod
    def from_dict(data: dict) -> Self:
        branch_length = data.pop("branch_length")
        branch_slope = data.pop("branch_slope")
        branch_interval = data.pop("branch_interval")
        branch_canopy = CanopyType.from_dict(data.pop("branch_canopy"))
        return MegaBranches(branch_length, branch_slope, branch_interval, branch_canopy)

    def jsonify(self) -> dict:
        data = {
            "branch_length": self.branch_length,
            "branch_slope": self.branch_slope,
            "branch_interval": self.branch_interval,
            "branch_canopy": self.branch_canopy.jsonify(),
        }
        return data


@dataclass
class TreeTypeWeights:
    one_branch: int
    two_branches: int
    two_branches_and_trunk: int

    @staticmethod
    def from_dict(data: dict) -> Self:
        return TreeTypeWeights(**data)

    def jsonify(self) -> dict:
        data = {
            "one_branch": self.one_branch,
            "two_branches": self.two_branches,
            "two_branches_and_trunk": self.two_branches_and_trunk,
        }
        return data


@dataclass
class CherryBranches:
    tree_type_weights: TreeTypeWeights
    branch_horizontal_length: int
    branch_start_offset_from_top: int
    branch_end_offset_from_top: int
    branch_canopy: CanopyType

    @staticmethod
    def from_dict(data: dict) -> Self:
        tree_type_weights = TreeTypeWeights.from_dict(data.pop("tree_type_weights"))
        branch_horizontal_length = data.pop("branch_horizontal_length")
        branch_start_offset_from_top = data.pop("branch_start_offset_from_top")
        branch_end_offset_from_top = data.pop("branch_end_offset_from_top")
        branch_canopy = CanopyType.from_dict(data.pop("branch_canopy"))
        return CherryBranches(
            tree_type_weights,
            branch_horizontal_length,
            branch_start_offset_from_top,
            branch_end_offset_from_top,
            branch_canopy,
        )

    def jsonify(self) -> dict:
        data = {
            "tree_type_weights": self.tree_type_weights.jsonify(),
            "branch_horizontal_length": self.branch_horizontal_length,
            "branch_start_offset_from_top": self.branch_start_offset_from_top,
            "branch_end_offset_from_top": self.branch_end_offset_from_top,
            "branch_canopy": self.branch_canopy.jsonify(),
        }
        return data


@dataclass
class FancyBranches:
    slope: float
    density: float
    min_altitude_factor: float

    @staticmethod
    def from_dict(data: dict) -> Self:
        return FancyBranches(**data)

    def jsonify(self) -> dict:
        data = {
            "slope": self.slope,
            "density": self.density,
            "min_altitude_factor": self.min_altitude_factor,
        }
        return data


@dataclass
class Decoration:
    decoration_block: BlockState
    decoration_chance: float
    num_steps: int = None
    step_direction: str = None

    @staticmethod
    def from_dict(data: dict) -> Self:
        decoration_block = BlockState.of(data.pop("decoration_block"))
        decoration_chance = data.pop("decoration_chance")
        num_steps = data.pop("num_steps") if "num_steps" in data else None
        step_direction = (
            data.pop("step_direction") if "step_direction" in data else None
        )
        return Decoration(
            decoration_block, decoration_chance, num_steps, step_direction
        )

    def jsonify(self) -> dict:
        data = {
            "decoration_block": self.decoration_block.jsonify(),
            "decoration_chance": self.decoration_chance,
        }
        if self.num_steps:
            data["num_steps"] = self.num_steps
        if self.step_direction:
            data["step_direction"] = self.step_direction
        return data


@dataclass
class TrunkType:
    trunk_block: BlockState

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier.of(value))

    @property
    def trunk_block(self) -> BlockState:
        return getattr(self, "_trunk_block")

    @trunk_block.setter
    def trunk_block(self, value: BlockState):
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_block", BlockState.of(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        return TrunkType(**data)

    def jsonify(self) -> dict:
        data = {"trunk_block": self.trunk_block.jsonify()}
        return data


class RootType:
    def __init__(self): ...

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier.of(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        for id in data.keys():
            clazz = INSTANCE.get_registry(Registries.TREE_ROOT).get(id)
            if clazz is not None:
                return clazz.from_dict(data)

    def jsonify(self) -> dict:
        data = {}
        return data


@dataclass
class AboveRoot:
    above_root_chance: float
    above_root_block: BlockState

    @staticmethod
    def from_dict(data: dict) -> Self:
        above_root_chance = data.pop("above_root_chance")
        above_root_block = BlockState.from_dict(data.pop("above_root_block"))
        return AboveRoot(above_root_chance, above_root_block)

    def jsonify(self) -> dict:
        data = {
            "above_root_chance": self.above_root_chance,
            "above_root_block": self.above_root_block.jsonify(),
        }
        return data


INSTANCE.create_registry(Registries.TREE_TRUNK, TrunkType)


def tree_trunk(cls):
    """
    Add this tree trunk to the registry
    """

    def wrapper():
        if not issubclass(cls, TrunkType):
            raise TypeError(f"Expected TrunkType but got '{cls.__name__}' instead")
        return INSTANCE.register(Registries.TREE_TRUNK, cls.id, cls)

    return wrapper()


INSTANCE.create_registry(Registries.TREE_CANOPY, CanopyType)


def tree_canopy(cls):
    """
    Add this tree canopy to the registry
    """

    def wrapper():
        if not issubclass(cls, CanopyType):
            raise TypeError(f"Expected CanopyType but got '{cls.__name__}' instead")
        return INSTANCE.register(Registries.TREE_CANOPY, cls.id, cls)

    return wrapper()


INSTANCE.create_registry(Registries.TREE_ROOT, RootType)


def tree_root(cls):
    """
    Add this tree misc to the registry
    """

    def wrapper():
        if not issubclass(cls, RootType):
            raise TypeError(f"Expected RootType but got '{cls.__name__}' instead")
        return INSTANCE.register(Registries.TREE_ROOT, cls.id, cls)

    return wrapper()


@tree_trunk
class Trunk(TrunkType):
    id = Identifier("trunk")

    def __init__(
        self,
        trunk_block: BlockState,
        trunk_height: TrunkHeight,
        height_modifier: int,
        can_be_submerged: int | bool,
        trunk_decoration: Decoration,
    ):
        TrunkType.__init__(self, trunk_block)
        # can_be_submerged {max_depth: int}
        self.trunk_height = trunk_height
        self.height_modifier = height_modifier
        self.can_be_submerged = can_be_submerged
        self.trunk_decoration = trunk_decoration

    @property
    def trunk_height(self) -> TrunkHeight | Range:
        return getattr(self, "_trunk_height")

    @trunk_height.setter
    def trunk_height(self, value: TrunkHeight | Range):
        if not isinstance(value, (TrunkHeight, Range)):
            raise TypeError(
                f"Expected TrunkHeight, Range but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_height", value)

    @property
    def height_modifier(self) -> Range:
        return getattr(self, "_height_modifier", None)

    @height_modifier.setter
    def height_modifier(self, value: Range):
        if value is None:
            return
        if not isinstance(value, Range):
            raise TypeError(
                f"Expected Range but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_height_modifier", value)

    @property
    def can_be_submerged(self) -> int | bool:
        return getattr(self, "_can_be_submerged", False)

    @can_be_submerged.setter
    def can_be_submerged(self, value: dict | bool):
        if value is None:
            return
        if not isinstance(value, (dict, bool)):
            raise TypeError(
                f"Expected dict, bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_can_be_submerged", value)

    @property
    def trunk_decoration(self) -> Decoration:
        return getattr(self, "_trunk_decoration", None)

    @trunk_decoration.setter
    def trunk_decoration(self, value: Decoration):
        if value is None:
            return
        if not isinstance(value, Decoration):
            raise TypeError(
                f"Expected Decoration but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_decoration", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        trunk_block = BlockState.from_dict(data.pop("trunk_block"))
        trunk_height = (
            Range.from_dict(data.pop("trunk_height"), "range_")
            if "range_min" in data["trunk_height"]
            else TrunkHeight.from_dict(data.pop("trunk_height"))
        )
        height_modifier = (
            Range.from_dict(data.pop("height_modifier"), "range_")
            if "height_modifier" in data
            else None
        )
        can_be_submerged = (
            data.pop("can_be_submerged") if "can_be_submerged" in data else None
        )
        trunk_decoration = (
            Decoration.from_dict(data.pop("trunk_decoration"))
            if "trunk_decoration" in data
            else None
        )
        return Trunk(
            trunk_block,
            trunk_height,
            height_modifier,
            can_be_submerged,
            trunk_decoration,
        )

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["trunk_height"] = self.trunk_height.jsonify("range_")
        data["can_be_submerged"] = self.can_be_submerged
        if self.height_modifier is not None:
            data["height_modifier"] = self.height_modifier.jsonify("range_")
        if self.trunk_decoration:
            data["trunk_decoration"] = self.trunk_decoration.jsonify()
        return data


@tree_trunk
class AcaciaTrunk(TrunkType):
    id = Identifier("acacia_trunk")

    def __init__(
        self,
        trunk_block: BlockState,
        trunk_height: TrunkHeight,
        trunk_width: int,
        trunk_lean: TrunkLean,
        branches: AcaciaBranches = None,
        trunk_decoration: Decoration = None,
    ):
        TrunkType.__init__(self, trunk_block)
        self.trunk_height = trunk_height
        self.trunk_width = trunk_width
        self.trunk_lean = trunk_lean
        self.branches = branches
        self.trunk_decoration = trunk_decoration

    @property
    def trunk_height(self) -> TrunkHeight:
        return getattr(self, "_trunk_height")

    @trunk_height.setter
    def trunk_height(self, value: TrunkHeight):
        if not isinstance(value, TrunkHeight):
            raise TypeError(
                f"Expected TrunkHeight but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_height", value)

    @property
    def trunk_width(self) -> int:
        return getattr(self, "_trunk_width")

    @trunk_width.setter
    def trunk_width(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_width", value)

    @property
    def trunk_lean(self) -> TrunkLean:
        return getattr(self, "_trunk_lean")

    @trunk_lean.setter
    def trunk_lean(self, value: TrunkLean):
        if value is None:
            return
        if not isinstance(value, TrunkLean):
            raise TypeError(
                f"Expected TrunkLean but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_lean", value)

    @property
    def branches(self) -> AcaciaBranches:
        return getattr(self, "_branches", None)

    @branches.setter
    def branches(self, value: AcaciaBranches):
        if value is None:
            return
        if not isinstance(value, AcaciaBranches):
            raise TypeError(
                f"Expected AcaciaBranches but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_branches", value)

    @property
    def trunk_decoration(self) -> Decoration:
        return getattr(self, "_trunk_decoration", None)

    @trunk_decoration.setter
    def trunk_decoration(self, value: Decoration):
        if value is None:
            return
        if not isinstance(value, Decoration):
            raise TypeError(
                f"Expected Decoration but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_decoration", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        trunk_block = BlockState.from_dict(data.pop("trunk_block"))
        trunk_height = TrunkHeight.from_dict(data.pop("trunk_height"))
        trunk_width = data.pop("trunk_width")
        trunk_lean = TrunkLean.from_dict(data.pop("trunk_lean"))
        branches = (
            AcaciaBranches.from_dict(data.pop("branches"))
            if "branches" in data
            else None
        )
        trunk_decoration = (
            Decoration.from_dict(data.pop("trunk_decoration"))
            if "trunk_decoration" in data
            else None
        )
        return AcaciaTrunk(
            trunk_block,
            trunk_height,
            trunk_width,
            trunk_lean,
            branches,
            trunk_decoration,
        )

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["trunk_height"] = self.trunk_height.jsonify()
        data["trunk_width"] = self.trunk_width
        data["trunk_lean"] = self.trunk_lean.jsonify()
        if self.branches:
            data["branches"] = self.branches.jsonify()
        if self.trunk_decoration:
            data["trunk_decoration"] = self.trunk_decoration.jsonify()
        return data


@tree_trunk
class CherryTrunk(TrunkType):
    id = Identifier("cherry_trunk")

    def __init__(
        self,
        trunk_block: BlockState,
        trunk_height: TrunkHeight,
        branches: CherryBranches,
    ):
        TrunkType.__init__(self, trunk_block)
        self.trunk_height = trunk_height
        self.branches = branches

    @property
    def trunk_height(self) -> TrunkHeight:
        return getattr(self, "_trunk_height")

    @trunk_height.setter
    def trunk_height(self, value: TrunkHeight):
        if not isinstance(value, TrunkHeight):
            raise TypeError(
                f"Expected TrunkHeight but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_height", value)

    @property
    def branches(self) -> CherryBranches:
        return getattr(self, "_branches")

    @branches.setter
    def branches(self, value: CherryBranches):
        if not isinstance(value, CherryBranches):
            raise TypeError(
                f"Expected CherryBranches but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_branches", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        trunk_block = BlockState.from_dict(data.pop("trunk_block"))
        trunk_height = TrunkHeight.from_dict(data.pop("trunk_height"))
        branches = CherryBranches.from_dict(data.pop("branches"))
        return CherryTrunk(trunk_block, trunk_height, branches)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["trunk_height"] = self.trunk_height.jsonify()
        data["branches"] = self.branches.jsonify()
        return data


@tree_trunk
class FallenTrunk(TrunkType):
    id = Identifier("fallen_trunk")

    def __init__(
        self,
        trunk_block: BlockState,
        log_length: int,
        stump_height: int,
        height_modifier: int,
        log_decoration_feature: Identifiable,
        trunk_decoration: Decoration,
    ):
        TrunkType.__init__(self, trunk_block)
        self.log_length = log_length
        self.stump_height = stump_height
        self.height_modifier = height_modifier
        self.log_decoration_feature = log_decoration_feature
        self.trunk_decoration = trunk_decoration

    @property
    def log_length(self) -> int | Range:
        return getattr(self, "_log_length")

    @log_length.setter
    def log_length(self, value: int | Range):
        if not isinstance(value, (int, Range)):
            raise TypeError(
                f"Expected int, Range but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_log_length", value)

    @property
    def stump_height(self) -> int:
        return getattr(self, "_stump_height", 1)

    @stump_height.setter
    def stump_height(self, value: int):
        if value is None:
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_stump_height", value)

    @property
    def height_modifier(self) -> Range:
        return getattr(self, "_height_modifier", None)

    @height_modifier.setter
    def height_modifier(self, value: Range):
        if value is None:
            return
        if not isinstance(value, Range):
            raise TypeError(
                f"Expected Range but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_height_modifier", value)

    @property
    def log_decoration_feature(self) -> Identifier:
        return getattr(self, "_log_decoration_feature")

    @log_decoration_feature.setter
    def log_decoration_feature(self, value: Identifiable):
        setattr(self, "_log_decoration_feature", Identifiable.of(value))

    @property
    def trunk_decoration(self) -> Decoration:
        return getattr(self, "_trunk_decoration", None)

    @trunk_decoration.setter
    def trunk_decoration(self, value: Decoration):
        if value is None:
            return
        if not isinstance(value, Decoration):
            raise TypeError(
                f"Expected Decoration but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_decoration", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        trunk_block = BlockState.from_dict(data.pop("trunk_block"))
        log_length = (
            Range.from_dict(data.pop("log_length"), "range_")
            if isinstance(data["log_length"], dict)
            else data.pop("log_length")
        )
        stump_height = data.pop("stump_height") if "stump_height" in data else None
        height_modifier = (
            Range.from_dict(data.pop("height_modifier"), "range_")
            if "height_modifier" in data
            else None
        )
        log_decoration_feature = data.pop("log_decoration_feature")
        trunk_decoration = (
            Decoration.from_dict(data.pop("trunk_decoration"))
            if "trunk_decoration" in data
            else None
        )
        return FallenTrunk(
            trunk_block,
            log_length,
            stump_height,
            height_modifier,
            log_decoration_feature,
            trunk_decoration,
        )

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["log_length"] = (
            self.log_length.jsonify("range_")
            if isinstance(self.log_length, Range)
            else self.log_length
        )
        data["log_decoration_feature"] = str(self.log_decoration_feature)
        if self.stump_height:
            data["stump_height"] = self.stump_height
        if self.height_modifier is not None:
            data["height_modifier"] = self.height_modifier.jsonify("range_")
        if self.trunk_decoration:
            data["trunk_decoration"] = self.trunk_decoration.jsonify()
        return data


@tree_trunk
class FancyTrunk(TrunkType):
    id = Identifier("fancy_trunk")

    def __init__(
        self,
        trunk_block: BlockState,
        trunk_height: FancyHeight,
        trunk_width: int,
        branches: FancyBranches,
        width_scale: float,
        foliage_altitude_factor: float,
    ):
        TrunkType.__init__(self, trunk_block)
        self.trunk_height = trunk_height
        self.trunk_width = trunk_width
        self.branches = branches
        self.width_scale = width_scale
        self.foliage_altitude_factor = foliage_altitude_factor

    @property
    def trunk_height(self) -> FancyHeight:
        return getattr(self, "_trunk_height")

    @trunk_height.setter
    def trunk_height(self, value: FancyHeight):
        if not isinstance(value, FancyHeight):
            raise TypeError(
                f"Expected FancyHeight but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_height", value)

    @property
    def trunk_width(self) -> int:
        return getattr(self, "_trunk_width")

    @trunk_width.setter
    def trunk_width(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_width", value)

    @property
    def branches(self) -> FancyBranches:
        return getattr(self, "_branches")

    @branches.setter
    def branches(self, value: FancyBranches):
        if not isinstance(value, FancyBranches):
            raise TypeError(
                f"Expected FancyBranches but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_branches", value)

    @property
    def width_scale(self) -> float:
        return getattr(self, "_width_scale")

    @width_scale.setter
    def width_scale(self, value: float):
        if not isinstance(value, float):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_width_scale", value)

    @property
    def foliage_altitude_factor(self) -> float:
        return getattr(self, "_foliage_altitude_factor")

    @foliage_altitude_factor.setter
    def foliage_altitude_factor(self, value: float):
        if not isinstance(value, float):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_foliage_altitude_factor", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        trunk_block = BlockState.from_dict(data.pop("trunk_block"))
        trunk_height = FancyHeight.from_dict(data.pop("trunk_height"))
        trunk_width = data.pop("trunk_width")
        branches = FancyBranches.from_dict(data.pop("branches"))
        width_scale = data.pop("width_scale")
        foliage_altitude_factor = data.pop("foliage_altitude_factor")
        return FancyTrunk(
            trunk_block,
            trunk_height,
            trunk_width,
            branches,
            width_scale,
            foliage_altitude_factor,
        )

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["trunk_height"] = self.trunk_height.jsonify()
        data["trunk_width"] = self.trunk_width
        data["branches"] = self.branches.jsonify()
        data["width_scale"] = self.width_scale
        data["foliage_altitude_factor"] = self.foliage_altitude_factor
        return data


@tree_trunk
class MangroveTrunk(TrunkType):
    id = Identifier("mangrove_trunk")

    def __init__(
        self,
        trunk_block: BlockState,
        trunk_height: MangroveHeight,
        trunk_width: int,
        branches: Branches,
        trunk_decoration: Decoration,
    ):
        TrunkType.__init__(self, trunk_block)
        self.trunk_height = trunk_height
        self.trunk_width = trunk_width
        self.branches = branches
        self.trunk_decoration = trunk_decoration

    @property
    def trunk_height(self) -> MangroveHeight:
        return getattr(self, "_trunk_height")

    @trunk_height.setter
    def trunk_height(self, value: MangroveHeight):
        if not isinstance(value, MangroveHeight):
            raise TypeError(
                f"Expected MangroveHeight but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_height", value)

    @property
    def trunk_width(self) -> int:
        return getattr(self, "_trunk_width")

    @trunk_width.setter
    def trunk_width(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_width", value)

    @property
    def branches(self) -> Branches:
        return getattr(self, "_branches")

    @branches.setter
    def branches(self, value: Branches):
        if not isinstance(value, Branches):
            raise TypeError(
                f"Expected Branches but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_branches", value)

    @property
    def trunk_decoration(self) -> Decoration:
        return getattr(self, "_trunk_decoration", None)

    @trunk_decoration.setter
    def trunk_decoration(self, value: Decoration):
        if value is None:
            return
        if not isinstance(value, Decoration):
            raise TypeError(
                f"Expected Decoration but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_decoration", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        trunk_block = BlockState.from_dict(data.pop("trunk_block"))
        trunk_height = MangroveHeight.from_dict(data.pop("trunk_height"))
        trunk_width = data.pop("trunk_width")
        branches = (
            Branches.from_dict(data.pop("branches")) if "branches" in data else None
        )
        trunk_decoration = (
            Decoration.from_dict(data.pop("trunk_decoration"))
            if "trunk_decoration" in data
            else None
        )
        return MangroveTrunk(
            trunk_block, trunk_height, trunk_width, branches, trunk_decoration
        )

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["trunk_height"] = self.trunk_height.jsonify()
        data["trunk_width"] = self.trunk_width
        data["branches"] = self.branches.jsonify()
        if self.trunk_decoration:
            data["trunk_decoration"] = self.trunk_decoration.jsonify()
        return data


@tree_trunk
class MegaTrunk(TrunkType):
    id = Identifier("mega_trunk")

    def __init__(
        self,
        trunk_block: BlockState,
        trunk_height: TrunkHeight,
        trunk_width: int,
        trunk_decoration: Decoration,
        branches: MegaBranches,
    ):
        TrunkType.__init__(self, trunk_block)
        self.trunk_height = trunk_height
        self.trunk_width = trunk_width
        self.trunk_decoration = trunk_decoration
        self.branches = branches

    @property
    def trunk_height(self) -> TrunkHeight:
        return getattr(self, "_trunk_height")

    @trunk_height.setter
    def trunk_height(self, value: TrunkHeight):
        if not isinstance(value, TrunkHeight):
            raise TypeError(
                f"Expected TrunkHeight but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_height", value)

    @property
    def trunk_width(self) -> int:
        return getattr(self, "_trunk_width")

    @trunk_width.setter
    def trunk_width(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_width", value)

    @property
    def trunk_decoration(self) -> Decoration:
        return getattr(self, "_trunk_decoration", None)

    @trunk_decoration.setter
    def trunk_decoration(self, value: Decoration):
        if value is None:
            return
        if not isinstance(value, Decoration):
            raise TypeError(
                f"Expected Decoration but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_decoration", value)

    @property
    def branches(self) -> MegaBranches:
        return getattr(self, "_branches", None)

    @branches.setter
    def branches(self, value: MegaBranches):
        if value is None:
            return
        if not isinstance(value, MegaBranches):
            raise TypeError(
                f"Expected MegaBranches but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_branches", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        trunk_block = BlockState.from_dict(data.pop("trunk_block"))
        trunk_height = TrunkHeight.from_dict(data.pop("trunk_height"))
        trunk_width = data.pop("trunk_width")
        trunk_decoration = (
            Decoration.from_dict(data.pop("trunk_decoration"))
            if "trunk_decoration" in data
            else None
        )
        branches = (
            MegaBranches.from_dict(data.pop("branches")) if "branches" in data else None
        )
        return MegaTrunk(
            trunk_block, trunk_height, trunk_width, trunk_decoration, branches
        )

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["trunk_height"] = self.trunk_height.jsonify()
        data["trunk_width"] = self.trunk_width
        if self.trunk_decoration:
            data["trunk_decoration"] = self.trunk_decoration.jsonify()
        if self.branches:
            data["branches"] = self.branches.jsonify()
        return data


@tree_canopy
class Canopy(CanopyType):
    id = Identifier("canopy")

    def __init__(
        self,
        leaf_block: BlockState,
        canopy_offset: Range,
        min_width: int,
        canopy_slope: Slope,
        variation_chance: float,
        canopy_decoration: Decoration,
    ):
        CanopyType.__init__(self)
        self.leaf_block = leaf_block
        self.canopy_offset = canopy_offset
        self.min_width = min_width
        self.canopy_slope = canopy_slope
        self.variation_chance = variation_chance
        self.canopy_decoration = canopy_decoration

    @property
    def leaf_block(self) -> BlockState:
        return getattr(self, "_leaf_block")

    @leaf_block.setter
    def leaf_block(self, value: BlockState):
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_leaf_block", value)

    @property
    def canopy_offset(self) -> Range:
        return getattr(self, "_canopy_offset")

    @canopy_offset.setter
    def canopy_offset(self, value: Range):
        if not isinstance(value, Range):
            raise TypeError(
                f"Expected Range but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_canopy_offset", value)

    @property
    def min_width(self) -> int:
        return getattr(self, "_min_width", None)

    @min_width.setter
    def min_width(self, value: int):
        if value is None:
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_min_width", value)

    @property
    def canopy_slope(self) -> Slope:
        return getattr(self, "_canopy_slope", None)

    @canopy_slope.setter
    def canopy_slope(self, value: Slope):
        if value is None:
            return
        if not isinstance(value, Slope):
            raise TypeError(
                f"Expected Slope but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_canopy_slope", value)

    @property
    def variation_chance(self) -> list:
        return getattr(self, "_variation_chance")

    @variation_chance.setter
    def variation_chance(self, value: list):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_variation_chance", value)

    @property
    def canopy_decoration(self) -> Decoration:
        return getattr(self, "_canopy_decoration", None)

    @canopy_decoration.setter
    def canopy_decoration(self, value: Decoration):
        if value is None:
            return
        if not isinstance(value, Decoration):
            raise TypeError(
                f"Expected Decoration but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_canopy_decoration", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        leaf_block = BlockState.from_dict(data.pop("leaf_block"))
        canopy_offset = Range.from_dict(data.pop("canopy_offset"))
        min_width = data.pop("min_width") if "min_width" in data else None
        canopy_slope = (
            Slope.from_dict(data.pop("canopy_slope"))
            if "canopy_slope" in data
            else None
        )
        variation_chance = data.pop("variation_chance")
        canopy_decoration = (
            Decoration.from_dict(data.pop("canopy_decoration"))
            if "canopy_decoration" in data
            else None
        )
        return Canopy(
            leaf_block,
            canopy_offset,
            min_width,
            canopy_slope,
            variation_chance,
            canopy_decoration,
        )

    def jsonify(self) -> dict:
        data = {
            "leaf_block": self.leaf_block.jsonify(),
            "canopy_offset": self.canopy_offset.jsonify(),
            "variation_chance": self.variation_chance,
        }
        if self.min_width:
            data["min_width"] = self.min_width
        if self.canopy_slope:
            data["canopy_slope"] = (self.canopy_slope.jsonify(),)
        if self.canopy_decoration:
            data["canopy_decoration"] = (self.canopy_decoration.jsonify(),)
        return data


@tree_canopy
class AcaciaCanopy(CanopyType):
    id = Identifier("acacia_canopy")

    def __init__(self, leaf_block: BlockState, canopy_size: int, simplify_canopy: bool):
        CanopyType.__init__(self)
        self.leaf_block = leaf_block
        self.canopy_size = canopy_size
        self.simplify_canopy = simplify_canopy

    @property
    def leaf_block(self) -> BlockState:
        return getattr(self, "_leaf_block")

    @leaf_block.setter
    def leaf_block(self, value: BlockState):
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_leaf_block", value)

    @property
    def canopy_size(self) -> int:
        return getattr(self, "_canopy_size")

    @canopy_size.setter
    def canopy_size(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_canopy_size", value)

    @property
    def simplify_canopy(self) -> bool:
        return getattr(self, "_simplify_canopy", False)

    @simplify_canopy.setter
    def simplify_canopy(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_simplify_canopy", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        leaf_block = BlockState.from_dict(data.pop("leaf_block"))
        canopy_size = data.pop("canopy_size")
        simplify_canopy = (
            data.pop("simplify_canopy") if "simplify_canopy" in data else False
        )
        return AcaciaCanopy(leaf_block, canopy_size, simplify_canopy)

    def jsonify(self) -> dict:
        data = {
            "leaf_block": self.leaf_block.jsonify(),
            "canopy_size": self.canopy_size,
            "simply_canopy": self.simplify_canopy,
        }
        return data


@tree_canopy
class CherryCanopy(CanopyType):
    id = Identifier("cherry_canopy")

    def __init__(
        self,
        leaf_block: BlockState,
        height: int,
        radius: int,
        trunk_width: int,
        wide_bottom_layer_hole_chance: float,
        corner_hole_chance: float,
        hanging_leaves_chance: float,
        hanging_leaves_extension_chance: float,
    ):
        CanopyType.__init__(self)
        self.leaf_block = leaf_block
        self.height = height
        self.radius = radius
        self.trunk_width = trunk_width
        self.wide_bottom_layer_hole_chance = wide_bottom_layer_hole_chance
        self.corner_hole_chance = corner_hole_chance
        self.hanging_leaves_chance = hanging_leaves_chance
        self.hanging_leaves_extension_chance = hanging_leaves_extension_chance

    @property
    def leaf_block(self) -> BlockState:
        return getattr(self, "_leaf_block")

    @leaf_block.setter
    def leaf_block(self, value: BlockState):
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_leaf_block", value)

    @property
    def height(self) -> int:
        return getattr(self, "_height")

    @height.setter
    def height(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_height", value)

    @property
    def radius(self) -> int:
        return getattr(self, "_radius")

    @radius.setter
    def radius(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_radius", value)

    @property
    def radius(self) -> int:
        return getattr(self, "_radius")

    @radius.setter
    def radius(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_radius", value)

    @property
    def trunk_width(self) -> int:
        return getattr(self, "_trunk_width", 1)

    @trunk_width.setter
    def trunk_width(self, value: int):
        if value is None:
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk_width", value)

    @property
    def wide_bottom_layer_hole_chance(self) -> float:
        return getattr(self, "_wide_bottom_layer_hole_chance")

    @wide_bottom_layer_hole_chance.setter
    def wide_bottom_layer_hole_chance(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float, int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_wide_bottom_layer_hole_chance", float(value))

    @property
    def corner_hole_chance(self) -> float:
        return getattr(self, "_corner_hole_chance")

    @corner_hole_chance.setter
    def corner_hole_chance(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float, int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_corner_hole_chance", float(value))

    @property
    def hanging_leaves_chance(self) -> float:
        return getattr(self, "_hanging_leaves_chance")

    @hanging_leaves_chance.setter
    def hanging_leaves_chance(self, value: float):
        if not isinstance(value, float):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_hanging_leaves_chance", value)

    @property
    def hanging_leaves_extension_chance(self) -> float:
        return getattr(self, "_hanging_leaves_extension_chance")

    @hanging_leaves_extension_chance.setter
    def hanging_leaves_extension_chance(self, value: float):
        if not isinstance(value, float):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_hanging_leaves_extension_chance", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        leaf_block = BlockState.from_dict(data.pop("leaf_block"))
        height = data.pop("height")
        radius = data.pop("radius")
        wide_bottom_layer_hole_chance = data.pop("wide_bottom_layer_hole_chance")
        corner_hole_chance = data.pop("corner_hole_chance")
        hanging_leaves_chance = data.pop("hanging_leaves_chance")
        hanging_leaves_extension_chance = data.pop("hanging_leaves_extension_chance")
        trunk_width = data.pop("trunk_width") if "trunk_width" in data else None
        return CherryCanopy(
            leaf_block,
            height,
            radius,
            trunk_width,
            wide_bottom_layer_hole_chance,
            corner_hole_chance,
            hanging_leaves_chance,
            hanging_leaves_extension_chance,
        )

    def jsonify(self) -> dict:
        data = {
            "leaf_block": self.leaf_block.jsonify(),
            "height": self.height,
            "radius": self.radius,
            "wide_bottom_layer_hole_chance": self.wide_bottom_layer_hole_chance,
            "corner_hole_chance": self.corner_hole_chance,
            "hanging_leaves_chance": self.hanging_leaves_chance,
            "hanging_leaves_extension_chance": self.hanging_leaves_extension_chance,
        }
        if self.trunk_width:
            data["trunk_width"] = self.trunk_width
        return data


@tree_canopy
class FancyCanopy(CanopyType):
    id = Identifier("fancy_canopy")

    def __init__(self, leaf_block: BlockState, height: int, radius: int):
        CanopyType.__init__(self)
        self.leaf_block = leaf_block
        self.height = height
        self.radius = radius

    @property
    def leaf_block(self) -> BlockState:
        return getattr(self, "_leaf_block")

    @leaf_block.setter
    def leaf_block(self, value: BlockState):
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_leaf_block", value)

    @property
    def height(self) -> int:
        return getattr(self, "_height")

    @height.setter
    def height(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_height", value)

    @property
    def radius(self) -> int:
        return getattr(self, "_radius")

    @radius.setter
    def radius(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_radius", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        leaf_block = BlockState.from_dict(data.pop("leaf_block"))
        height = data.pop("height")
        radius = data.pop("radius")
        return FancyCanopy(leaf_block, height, radius)

    def jsonify(self) -> dict:
        data = {
            "leaf_block": self.leaf_block.jsonify(),
            "height": self.height,
            "radius": self.radius,
        }
        return data


@tree_canopy
class MangroveCanopy(CanopyType):
    id = Identifier("mangrove_canopy")

    def __init__(
        self,
        canopy_height: int,
        canopy_radius: int,
        leaf_placement_attempts: int,
        leaf_blocks: list[BlockState],
        canopy_decoration: Decoration,
        hanging_block: BlockState,
        hanging_block_placement_chance: float,
    ):
        CanopyType.__init__(self)
        self.canopy_height = canopy_height
        self.canopy_radius = canopy_radius
        self.leaf_placement_attempts = leaf_placement_attempts
        self.leaf_blocks = leaf_blocks
        self.canopy_decoration = canopy_decoration
        self.hanging_block = hanging_block
        self.hanging_block_placement_chance = hanging_block_placement_chance

    @property
    def canopy_height(self) -> int:
        return getattr(self, "_canopy_height")

    @canopy_height.setter
    def canopy_height(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_canopy_height", value)

    @property
    def canopy_radius(self) -> int:
        return getattr(self, "_canopy_radius")

    @canopy_radius.setter
    def canopy_radius(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_canopy_radius", value)

    @property
    def leaf_placement_attempts(self) -> int:
        return getattr(self, "_leaf_placement_attempts")

    @leaf_placement_attempts.setter
    def leaf_placement_attempts(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_leaf_placement_attempts", value)

    @property
    def leaf_blocks(self) -> list[WeightedBlock]:
        return getattr(self, "_leaf_blocks")

    @leaf_blocks.setter
    def leaf_blocks(self, value: list[WeightedBlock]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_leaf_blocks", value)

    @property
    def hanging_block(self) -> BlockState:
        return getattr(self, "_hanging_block")

    @hanging_block.setter
    def hanging_block(self, value: BlockState):
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_hanging_block", value)

    @property
    def hanging_block_placement_chance(self) -> Chance:
        return getattr(self, "_hanging_block_placement_chance")

    @hanging_block_placement_chance.setter
    def hanging_block_placement_chance(self, value: Chance):
        if not isinstance(value, Chance):
            raise TypeError(
                f"Expected Chance but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_hanging_block_placement_chance", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        canopy_height = data.pop("canopy_height")
        canopy_radius = data.pop("canopy_radius")
        leaf_placement_attempts = data.pop("leaf_placement_attempts")
        leaf_blocks = [WeightedBlock.from_dict(x) for x in data.pop("leaf_blocks")]
        canopy_decoration = Decoration.from_dict(data.pop("canopy_decoration"))
        hanging_block = BlockState.from_dict(data.pop("hanging_block"))
        hanging_block_placement_chance = Chance.from_dict(
            data.pop("hanging_block_placement_chance")
        )
        return MangroveCanopy(
            canopy_height,
            canopy_radius,
            leaf_placement_attempts,
            leaf_blocks,
            canopy_decoration,
            hanging_block,
            hanging_block_placement_chance,
        )

    def jsonify(self) -> dict:
        data = {
            "canopy_height": self.canopy_height,
            "canopy_radius": self.canopy_radius,
            "leaf_placement_attempts": self.leaf_placement_attempts,
            "leaf_blocks": [x.jsonify() for x in self.leaf_blocks],
            "canopy_decoration": self.canopy_decoration.jsonify(),
            "hanging_block": self.hanging_block.jsonify(),
            "hanging_block_placement_chance": self.hanging_block_placement_chance.jsonify(),
        }
        return data


@tree_canopy
class MegaCanopy(CanopyType):
    id = Identifier("mega_canopy")

    def __init__(
        self,
        leaf_block: BlockState,
        canopy_height: int,
        base_radius: int,
        core_width: int,
        simplify_canopy: bool,
    ):
        CanopyType.__init__(self)
        self.leaf_block = leaf_block
        self.canopy_height = canopy_height
        self.base_radius = base_radius
        self.core_width = core_width
        self.simplify_canopy = simplify_canopy

    @property
    def leaf_block(self) -> BlockState:
        return getattr(self, "_leaf_block", None)

    @leaf_block.setter
    def leaf_block(self, value: BlockState):
        if value is None:
            return
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_leaf_block", value)

    @property
    def canopy_height(self) -> int | Range:
        return getattr(self, "_canopy_height", None)

    @canopy_height.setter
    def canopy_height(self, value: int | Range):
        if value is None:
            return
        if not isinstance(value, (int, Range)):
            raise TypeError(
                f"Expected Range, int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_canopy_height", value)

    @property
    def base_radius(self) -> int:
        return getattr(self, "_base_radius")

    @base_radius.setter
    def base_radius(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_base_radius", value)

    @property
    def core_width(self) -> int:
        return getattr(self, "_core_width", None)

    @core_width.setter
    def core_width(self, value: int):
        if value is None:
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_core_width", value)

    @property
    def simplify_canopy(self) -> bool:
        return getattr(self, "_simplify_canopy", False)

    @simplify_canopy.setter
    def simplify_canopy(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_simplify_canopy", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        leaf_block = BlockState.from_dict(data.pop("leaf_block"))
        canopy_height = Range.from_dict(data.pop("canopy_height"), "range_")
        base_radius = data.pop("base_radius")
        core_width = data.pop("core_width") if "core_width" in data else None
        simplify_canopy = (
            data.pop("simplify_canopy") if "simplify_canopy" in data else False
        )
        return MegaCanopy(
            leaf_block, canopy_height, base_radius, core_width, simplify_canopy
        )

    def jsonify(self) -> dict:
        data = {
            "base_radius": self.base_radius,
            "canopy_height": (
                self.canopy_height.jsonify("range_")
                if isinstance(self.canopy_height, Range)
                else self.canopy_height
            ),
            "leaf_block": self.leaf_block.jsonify(),
        }
        if self.core_width:
            data["core_width"] = self.core_width
        if self.simplify_canopy:
            data["simplify_canopy"] = self.simplify_canopy
        return data


@tree_canopy
class MegaPineCanopy(CanopyType):
    id = Identifier("mega_pine_canopy")

    def __init__(
        self,
        leaf_block: BlockState,
        canopy_height: int,
        base_radius: int,
        radius_step_modifier: float,
        core_width: int,
    ):
        CanopyType.__init__(self)
        self.leaf_block = leaf_block
        self.canopy_height = canopy_height
        self.base_radius = base_radius
        self.radius_step_modifier = radius_step_modifier
        self.core_width = core_width

    @property
    def leaf_block(self) -> BlockState:
        return getattr(self, "_leaf_block")

    @leaf_block.setter
    def leaf_block(self, value: BlockState):
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_leaf_block", value)

    @property
    def canopy_height(self) -> Range:
        return getattr(self, "_canopy_height")

    @canopy_height.setter
    def canopy_height(self, value: Range):
        if not isinstance(value, Range):
            raise TypeError(
                f"Expected Range but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_canopy_height", value)

    @property
    def base_radius(self) -> int:
        return getattr(self, "_base_radius")

    @base_radius.setter
    def base_radius(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_base_radius", value)

    @property
    def radius_step_modifier(self) -> float:
        return getattr(self, "_radius_step_modifier")

    @radius_step_modifier.setter
    def radius_step_modifier(self, value: float):
        if not isinstance(value, float):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_radius_step_modifier", value)

    @property
    def core_radius(self) -> int:
        return getattr(self, "_core_radius")

    @core_radius.setter
    def core_radius(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_core_radius", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        leaf_block = BlockState.from_dict(data.pop("leaf_block"))
        canopy_height = Range.from_dict(data.pop("canopy_height"), "range_")
        base_radius = data.pop("base_radius")
        radius_step_modifier = data.pop("radius_step_modifier")
        core_width = data.pop("core_width")
        return MegaPineCanopy(
            leaf_block, canopy_height, base_radius, radius_step_modifier, core_width
        )

    def jsonify(self) -> dict:
        data = {
            "leaf_block": self.leaf_block.jsonify(),
            "canopy_height": self.canopy_height.jsonify("range_"),
            "base_radius": self.base_radius,
            "radius_step_modifier": self.radius_step_modifier,
            "core_width": self.core_width,
        }
        return data


@tree_canopy
class PineCanopy(CanopyType):
    id = Identifier("pine_canopy")

    def __init__(self, leaf_block: BlockState, canopy_height: int, base_radius: int):
        CanopyType.__init__(self)
        self.leaf_block = leaf_block
        self.canopy_height = canopy_height
        self.base_radius = base_radius

    @property
    def leaf_block(self) -> BlockState:
        return getattr(self, "_leaf_block")

    @leaf_block.setter
    def leaf_block(self, value: BlockState):
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_leaf_block", value)

    @property
    def canopy_height(self) -> int | Range:
        return getattr(self, "_canopy_height")

    @canopy_height.setter
    def canopy_height(self, value: int | Range):
        if not isinstance(value, (int, Range)):
            raise TypeError(
                f"Expected int, Range but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_canopy_height", value)

    @property
    def base_radius(self) -> int:
        return getattr(self, "_base_radius")

    @base_radius.setter
    def base_radius(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_base_radius", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        leaf_block = BlockState.from_dict(data.pop("leaf_block"))
        canopy_height = Range.from_dict(data.pop("canopy_height"), "range_")
        base_radius = data.pop("base_radius")
        return PineCanopy(leaf_block, canopy_height, base_radius)

    def jsonify(self) -> dict:
        data = {
            "leaf_block": self.leaf_block.jsonify(),
            "canopy_height": (
                self.canopy_height.jsonify("range_")
                if isinstance(self.canopy_height, Range)
                else self.canopy_height
            ),
            "base_radius": self.base_radius,
        }
        return data


@tree_canopy
class RoofedCanopy(CanopyType):
    id = Identifier("roofed_canopy")

    def __init__(
        self,
        leaf_block: BlockState,
        canopy_height: int,
        core_width: int,
        outer_radius: int,
        inner_radius: int,
    ):
        CanopyType.__init__(self)
        self.leaf_block = leaf_block
        self.canopy_height = canopy_height
        self.core_width = core_width
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius

    @property
    def leaf_block(self) -> BlockState:
        return getattr(self, "_leaf_block")

    @leaf_block.setter
    def leaf_block(self, value: BlockState):
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_leaf_block", value)

    @property
    def canopy_height(self) -> int:
        return getattr(self, "_canopy_height")

    @canopy_height.setter
    def canopy_height(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_canopy_height", value)

    @property
    def core_width(self) -> int:
        return getattr(self, "_core_width")

    @core_width.setter
    def core_width(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_core_width", value)

    @property
    def outer_radius(self) -> int:
        return getattr(self, "_outer_radius")

    @outer_radius.setter
    def outer_radius(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_outer_radius", value)

    @property
    def inner_radius(self) -> int:
        return getattr(self, "_inner_radius")

    @inner_radius.setter
    def inner_radius(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_inner_radius", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        leaf_block = BlockState.from_dict(data.pop("leaf_block"))
        canopy_height = data.pop("canopy_height")
        core_width = data.pop("core_width")
        outer_radius = data.pop("outer_radius")
        inner_radius = data.pop("inner_radius")
        return RoofedCanopy(
            leaf_block, canopy_height, core_width, outer_radius, inner_radius
        )

    def jsonify(self) -> dict:
        data = {
            "leaf_block": self.leaf_block.jsonify(),
            "canopy_height": self.canopy_height,
            "core_width": self.core_width,
            "outer_radius": self.outer_radius,
            "inner_radius": self.inner_radius,
        }
        return data


@tree_canopy
class SpruceCanopy(CanopyType):
    id = Identifier("spruce_canopy")

    def __init__(
        self,
        leaf_block: BlockState,
        lower_offset: int,
        upper_offset: int,
        max_radius: int,
    ):
        CanopyType.__init__(self)
        self.leaf_block = leaf_block
        self.lower_offset = lower_offset
        self.upper_offset = upper_offset
        self.max_radius = max_radius

    @property
    def leaf_block(self) -> BlockState:
        return getattr(self, "_leaf_block")

    @leaf_block.setter
    def leaf_block(self, value: BlockState):
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_leaf_block", value)

    @property
    def lower_offset(self) -> Range:
        return getattr(self, "_lower_offset")

    @lower_offset.setter
    def lower_offset(self, value: Range):
        if not isinstance(value, Range):
            raise TypeError(
                f"Expected Range but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_lower_offset", value)

    @property
    def upper_offset(self) -> Range:
        return getattr(self, "_upper_offset")

    @upper_offset.setter
    def upper_offset(self, value: Range):
        if not isinstance(value, Range):
            raise TypeError(
                f"Expected Range but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_upper_offset", value)

    @property
    def max_radius(self) -> Range:
        return getattr(self, "_max_radius")

    @max_radius.setter
    def max_radius(self, value: Range):
        if not isinstance(value, Range):
            raise TypeError(
                f"Expected Range but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_max_radius", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        leaf_block = BlockState.from_dict(data.pop("leaf_block"))
        lower_offset = Range.from_dict(data.pop("lower_offset"), "range_")
        upper_offset = Range.from_dict(data.pop("upper_offset"), "range_")
        max_radius = Range.from_dict(data.pop("max_radius"), "range_")
        return SpruceCanopy(leaf_block, lower_offset, upper_offset, max_radius)

    def jsonify(self) -> dict:
        data = {
            "leaf_block": self.leaf_block.jsonify(),
            "lower_offset": self.lower_offset.jsonify("range_"),
            "upper_offset": self.upper_offset.jsonify("range_"),
            "max_radius": self.max_radius.jsonify("range_"),
        }
        return data


@tree_canopy
class RandomSpreadCanopy(CanopyType):
    id = Identifier("random_spread_canopy")

    def __init__(
        self,
        canopy_height: int,
        canopy_radius: int,
        leaf_placement_attemps: int,
        leaf_blocks: list[WeightedBlock] = [],
    ):
        CanopyType.__init__(self)
        self.leaf_blocks = leaf_blocks
        self.canopy_height = canopy_height
        self.canopy_radius = canopy_radius
        self.leaf_placement_attemps = leaf_placement_attemps

    @property
    def leaf_blocks(self) -> list[WeightedBlock]:
        return getattr(self, "_leaf_blocks")

    @leaf_blocks.setter
    def leaf_blocks(self, value: list[WeightedBlock]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_leaf_blocks", value)

    @property
    def canopy_height(self) -> int:
        return getattr(self, "_canopy_height")

    @canopy_height.setter
    def canopy_height(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_canopy_height", value)

    @property
    def canopy_radius(self) -> int:
        return getattr(self, "_canopy_radius")

    @canopy_radius.setter
    def canopy_radius(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_canopy_radius", value)

    @property
    def leaf_placement_attempts(self) -> int:
        return getattr(self, "_leaf_placement_attempts")

    @leaf_placement_attempts.setter
    def leaf_placement_attempts(self, value: int):
        if value is None:
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_leaf_placement_attempts", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        leaf_blocks = [WeightedBlock.from_dict(x) for x in data.pop("leaf_blocks")]
        canopy_height = data.pop("canopy_height")
        canopy_radius = data.pop("canopy_radius")
        leaf_placement_attemps = (
            data.pop("leaf_placement_attemps")
            if "leaf_placement_attemps" in data
            else None
        )
        return RandomSpreadCanopy(
            canopy_height, canopy_radius, leaf_placement_attemps, leaf_blocks
        )

    def jsonify(self) -> dict:
        data = {
            "leaf_blocks": [x.jsonify() for x in self.leaf_blocks],
            "canopy_height": self.canopy_height,
            "canopy_radius": self.canopy_radius,
            "leaf_placement_attemps": self.leaf_placement_attemps,
        }
        return data

    # LEAF BLOCK
    def get_leaf(self, index: int) -> WeightedBlock:
        return self.leaf_blocks[index]

    def add_leaf(self, block: WeightedBlock) -> WeightedBlock:
        self.leaf_blocks.append(block)
        return block

    def remove_leaf(self, index: int) -> WeightedBlock:
        return self.leaf_blocks.pop(index)

    def clear_leaves(self) -> Self:
        return self


@tree_root
class MangroveRoots(RootType):
    id = Identifier("mangrove_roots")

    def __init__(
        self,
        root_block: BlockState,
        max_root_width: int,
        max_root_length: int,
        above_root: AboveRoot,
        muddy_root_block: BlockState,
        mud_block: BlockState,
        y_offset: int,
        roots_may_grow_through: list[Identifiable],
        root_decoration: Decoration,
    ):
        RootType.__init__(self)
        self.root_block = root_block
        self.max_root_width = max_root_width
        self.max_root_length = max_root_length
        self.above_root = above_root
        self.muddy_root_block = muddy_root_block
        self.mud_block = mud_block
        self.y_offset = y_offset
        self.roots_may_grow_through = roots_may_grow_through
        self.root_decoration = root_decoration

    @property
    def root_block(self) -> BlockState:
        return getattr(self, "_root_block")

    @root_block.setter
    def root_block(self, value: BlockState):
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_root_block", value)

    @property
    def max_root_width(self) -> int:
        return getattr(self, "_max_root_width")

    @max_root_width.setter
    def max_root_width(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_max_root_width", value)

    @property
    def max_root_length(self) -> int:
        return getattr(self, "_max_root_length")

    @max_root_length.setter
    def max_root_length(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_max_root_length", value)

    @property
    def above_root(self) -> AboveRoot:
        return getattr(self, "_above_root")

    @above_root.setter
    def above_root(self, value: AboveRoot):
        if not isinstance(value, AboveRoot):
            raise TypeError(
                f"Expected AboveRoot but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_above_root", value)

    @property
    def muddy_mangrove_roots(self) -> BlockState:
        return getattr(self, "_muddy_mangrove_roots")

    @muddy_mangrove_roots.setter
    def muddy_mangrove_roots(self, value: BlockState):
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_muddy_mangrove_roots", value)

    @property
    def mud_block(self) -> BlockState:
        return getattr(self, "_mud_block")

    @mud_block.setter
    def mud_block(self, value: BlockState):
        if not isinstance(value, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_mud_block", value)

    @property
    def y_offset(self) -> int | Range:
        return getattr(self, "_y_offset")

    @y_offset.setter
    def y_offset(self, value: int | Range):
        if not isinstance(value, (int, Range)):
            raise TypeError(
                f"Expected int, Range but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_y_offset", value)

    @property
    def roots_may_grow_through(self) -> list[BlockState]:
        return getattr(self, "_roots_may_grow_through")

    @roots_may_grow_through.setter
    def roots_may_grow_through(self, value: list[BlockState]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_roots_may_grow_through", [BlockState.of(x) for x in value])

    @property
    def root_decoration(self) -> Decoration:
        return getattr(self, "_root_decoration", None)

    @root_decoration.setter
    def root_decoration(self, value: Decoration):
        if value is None:
            return
        if not isinstance(value, Decoration):
            raise TypeError(
                f"Expected Decoration but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_root_decoration", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        root_block = BlockState.from_dict(data.pop("root_block"))
        max_root_width = data.pop("max_root_width")
        max_root_length = data.pop("max_root_length")
        above_root = AboveRoot.from_dict(data.pop("above_root"))
        muddy_root_block = BlockState.from_dict(data.pop("muddy_root_block"))
        mud_block = BlockState.from_dict(data.pop("mud_block"))
        y_offset = Range.from_dict(data.pop("y_offset"), "range_")
        roots_may_grow_through = [
            BlockState.from_dict(x) for x in data.pop("roots_may_grow_through")
        ]
        root_decoration = (
            Decoration.from_dict(data.pop("root_decoration"))
            if "root_decoration" in data
            else None
        )
        return MangroveRoots(
            root_block,
            max_root_width,
            max_root_length,
            above_root,
            muddy_root_block,
            mud_block,
            y_offset,
            roots_may_grow_through,
            root_decoration,
        )

    def jsonify(self) -> dict:
        data = {
            "root_block": self.root_block.jsonify(),
            "max_root_width": self.max_root_width,
            "max_root_length": self.max_root_length,
            "above_root": self.above_root.jsonify(),
            "muddy_root_block": self.muddy_root_block.jsonify(),
            "mud_block": self.mud_block.jsonify(),
            "y_offset": (
                self.y_offset.jsonify("range_")
                if isinstance(self.y_offset, Range)
                else self.y_offset
            ),
            "roots_may_grow_through": [
                x.jsonify() for x in self.roots_may_grow_through
            ],
        }
        if self.root_decoration:
            data["root_decoration"] = (self.root_decoration.jsonify(),)
        return data


@feature_type
@behavior_pack
class TreeFeature(Feature):
    """
    Represents a data-driven [Tree Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Atree_feature).
    """

    id = Identifier("tree_feature")
    FILEPATH = "features/tree_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        trunk: Trunk = None,
        canopy: Canopy = None,
        root: RootType = None,
        base_cluster: Cluster = None,
        base_block: list[Identifiable] = [],
        may_grow_on: list[BlockPredicate] = [],
        may_replace: list[BlockPredicate] = [],
        may_grow_through: list[BlockPredicate] = [],
    ):
        Feature.__init__(self, identifier)
        self.base_block = base_block
        self.base_cluster = base_cluster
        self.may_grow_on = may_grow_on
        self.may_replace = may_replace
        self.may_grow_through = may_grow_through
        self.trunk = trunk
        self.canopy = canopy
        self.root = root

    @property
    def base_block(self) -> list[BlockState]:
        return getattr(self, "_base_block")

    @base_block.setter
    def base_block(self, value: list[BlockState]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_base_block", [BlockState.of(x) for x in value])

    @property
    def base_cluster(self) -> Cluster:
        return getattr(self, "_base_cluster", None)

    @base_cluster.setter
    def base_cluster(self, value: Cluster):
        if value is None:
            return
        if not isinstance(value, Cluster):
            raise TypeError(
                f"Expected Cluster but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_base_cluster", value)

    @property
    def may_grow_on(self) -> list[BlockPredicate]:
        return getattr2(self, "_may_grow_on", [])

    @may_grow_on.setter
    def may_grow_on(self, value: list[BlockPredicate]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_may_grow_on", [BlockPredicate.of(x) for x in value])

    @property
    def may_replace(self) -> list[BlockPredicate]:
        return getattr2(self, "_may_replace", [])

    @may_replace.setter
    def may_replace(self, value: list[BlockPredicate]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_may_replace", [BlockPredicate.of(x) for x in value])

    @property
    def may_grow_through(self) -> list[BlockPredicate]:
        return getattr2(self, "_may_grow_through", [])

    @may_grow_through.setter
    def may_grow_through(self, value: list[BlockPredicate]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_may_grow_through", [BlockPredicate.of(x) for x in value])

    @property
    def trunk(self) -> TrunkType:
        return getattr(self, "_trunk")

    @trunk.setter
    def trunk(self, value: TrunkType):
        if value is None:
            return
        if not isinstance(value, TrunkType):
            raise TypeError(
                f"Expected TrunkType but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trunk", value)

    @property
    def canopy(self) -> CanopyType:
        return getattr(self, "_canopy", None)

    @canopy.setter
    def canopy(self, value: CanopyType):
        if value is None:
            return
        if not isinstance(value, CanopyType):
            raise TypeError(
                f"Expected CanopyType but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_canopy", value)

    @property
    def root(self) -> RootType:
        return getattr(self, "_root", None)

    @root.setter
    def root(self, value: RootType):
        if value is None:
            return
        if not isinstance(value, RootType):
            raise TypeError(
                f"Expected RootType but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_root", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = TreeFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["base_block"] = [x.jsonify() for x in self.base_block]
        data[str(self.id)]["may_grow_on"] = [x.jsonify() for x in self.may_grow_on]
        data[str(self.id)]["may_replace"] = [x.jsonify() for x in self.may_replace]
        data[str(self.id)]["may_grow_through"] = [
            x.jsonify() for x in self.may_grow_through
        ]
        if self.base_cluster:
            data[str(self.id)]["base_cluster"] = self.base_cluster.jsonify()

        if self.trunk:
            data[str(self.id)][self.trunk.id.path] = self.trunk.jsonify()

        if self.canopy:
            data[str(self.id)][self.canopy.id.path] = self.canopy.jsonify()

        if self.root:
            data[str(self.id)][self.root.id.path] = self.root.jsonify()
        return data

    # BASE BLOCK
    def get_base_block(self, index: int) -> BlockState:
        return self.base_block[index]

    def add_base_block(self, block: BlockState) -> BlockState:
        b = BlockState.of(block)
        self.base_block.append(b)
        return b

    def remove_base_block(self, index: int) -> BlockState:
        return self.base_block.pop(index)

    def clear_base_blocks(self) -> Self:
        self.base_block.clear()
        return self

    # MAY GROW ON

    def get_grow_on(self, index: int) -> BlockState:
        return self.may_grow_on[index]

    def add_grow_on(self, block: BlockState) -> BlockState:
        b = BlockState.of(block)
        self.may_grow_on.append(b)
        return b

    def remove_grow_on(self, index: int) -> BlockState:
        return self.may_grow_on.pop(index)

    def clear_grow_on(self) -> Self:
        self.may_grow_on.clear()
        return self

    # MAY REPLACE

    def get_replace(self, index: int) -> BlockState:
        return self.may_replace[index]

    def add_replace(self, block: BlockState) -> BlockState:
        b = BlockState.of(block)
        self.may_replace.append(b)
        return b

    def remove_replace(self, index: int) -> BlockState:
        return self.may_replace.pop(index)

    def clear_replace(self) -> Self:
        self.may_replace.clear()
        return self

    # MAY GROW THROUGH

    def get_grow_through(self, index: int) -> BlockState:
        return self.may_grow_through[index]

    def add_grow_through(self, block: BlockState) -> BlockState:
        b = BlockState.of(block)
        self.may_grow_through.append(b)
        return b

    def remove_grow_through(self, index: int) -> BlockState:
        return self.may_grow_through.pop(index)

    def clear_grow_through(self) -> Self:
        self.may_grow_through.clear()
        return self


class TreeFeatureLoader(Loader):
    name = "Tree Feature"

    def __init__(self):
        from .schemas import TreeSchem1

        Loader.__init__(self, TreeFeature)
        self.add_schema(TreeSchem1, "1.13.0")
        self.add_schema(TreeSchem1, "1.16.0")


@feature_type
@behavior_pack
class VegetationPatchFeature(Feature):
    """
    Represents a data-driven [Vegetation Patch Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Avegetation_patch_feature).
    """

    id = Identifier("vegetation_patch_feature")
    FILEPATH = "features/vegetation_patch_feature.json"

    def __init__(
        self,
        identifier: Identifiable,
        ground_block: BlockState,
        vegetation_feature: Identifiable,
        surface: str,
        depth: Range,
        vertical_range: int,
        vegetation_chance: float,
        horizontal_radius: Range,
        extra_deep_block_chance: float,
        extra_edge_column_chance: float,
        waterlogged: bool,
        replaceable_blocks: list[BlockState] = [],
    ):
        Feature.__init__(self, identifier)
        self.replaceable_blocks = replaceable_blocks
        self.ground_block = ground_block
        self.vegetation_feature = vegetation_feature
        self.surface = surface
        self.depth = depth
        self.vertical_range = vertical_range
        self.vegetation_chance = vegetation_chance
        self.horizontal_radius = horizontal_radius
        self.extra_deep_block_chance = extra_deep_block_chance
        self.extra_deep_column_chance = extra_edge_column_chance
        self.waterlogged = waterlogged

    @property
    def waterlogged(self) -> bool:
        return getattr(self, "_waterlogged")

    @waterlogged.setter
    def waterlogged(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_waterlogged", value)

    @property
    def extra_deep_column_chance(self) -> float:
        return getattr(self, "_extra_deep_column_chance")

    @extra_deep_column_chance.setter
    def extra_deep_column_chance(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_extra_deep_column_chance", float(value))

    @property
    def extra_deep_block_chance(self) -> float:
        return getattr(self, "_extra_deep_block_chance", None)

    @extra_deep_block_chance.setter
    def extra_deep_block_chance(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_extra_deep_block_chance", float(value))

    @property
    def horizontal_radius(self) -> Range:
        return getattr(self, "_horizontal_radius")

    @horizontal_radius.setter
    def horizontal_radius(self, value: Range):
        if not isinstance(value, Range):
            raise TypeError(
                f"Expected Range but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_horizontal_radius", value)

    @property
    def vegetation_feature(self) -> Identifier:
        return getattr(self, "_vegetation_feature")

    @vegetation_feature.setter
    def vegetation_feature(self, value: Identifiable):
        setattr(self, "_vegetation_feature", Identifiable.of(value))

    @property
    def depth(self) -> Range | int:
        return getattr(self, "_depth")

    @depth.setter
    def depth(self, value: Range | int):
        if not isinstance(value, (Range, int)):
            raise TypeError(
                f"Expected Range, int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_depth", value)

    @property
    def vertical_range(self) -> int:
        return getattr(self, "_vertical_range")

    @vertical_range.setter
    def vertical_range(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_vertical_range", value)

    @property
    def surface(self) -> str:
        return getattr(self, "_surface")

    @surface.setter
    def surface(self, value: str):
        setattr(self, "_surface", str(value))

    @property
    def replaceable_blocks(self) -> list[BlockState]:
        return getattr(self, "_replaceable_blocks")

    @replaceable_blocks.setter
    def replaceable_blocks(self, value: list[BlockState]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_replaceable_blocks", [BlockState.of(x) for x in value])

    @property
    def vegetation_chance(self) -> float:
        return getattr(self, "_vegetation_chance")

    @vegetation_chance.setter
    def vegetation_chance(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_vegetation_chance", float(value))

    @property
    def ground_block(self) -> BlockState:
        return getattr(self, "_ground_block")

    @ground_block.setter
    def ground_block(self, value: BlockState):
        setattr(self, "_ground_block", BlockState.of(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = VegetationPatchFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["replaceable_blocks"] = [
            x.jsonify() for x in self.replaceable_blocks
        ]
        data[str(self.id)]["ground_block"] = self.ground_block.jsonify()
        data[str(self.id)]["vegetation_feature"] = str(self.vegetation_feature)
        data[str(self.id)]["surface"] = self.surface
        data[str(self.id)]["depth"] = (
            self.depth.jsonify("range_")
            if isinstance(self.depth, Range)
            else self.depth
        )
        data[str(self.id)]["vertical_range"] = self.vertical_range
        data[str(self.id)]["vegetation_chance"] = self.vegetation_chance
        data[str(self.id)]["horizontal_radius"] = self.horizontal_radius.jsonify(
            "range_"
        )
        if self.extra_deep_block_chance:
            data[str(self.id)]["extra_deep_block_chance"] = self.extra_deep_block_chance
        data[str(self.id)]["extra_deep_column_chance"] = self.extra_deep_column_chance
        return data

    def get_replace(self, index: int) -> BlockState:
        return self.replaceable_blocks[index]

    def add_replace(self, block: BlockState) -> BlockState:
        b = BlockState.of(block)
        self.replaceable_blocks.append(b)
        return b

    def remove_replace(self, index: int) -> BlockState:
        return self.replaceable_blocks.pop(index)

    def clear_replaces(self) -> Self:
        self.replaceable_blocks.clear()
        return self


class VegetationPatchFeatureLoader(Loader):
    name = "Vegetation Patch Feature"

    def __init__(self):
        from .schemas import VegetationPatchSchem1

        Loader.__init__(self, VegetationPatchFeature)
        self.add_schema(VegetationPatchSchem1, "1.13.0")
        self.add_schema(VegetationPatchSchem1, "1.16.0")


class WeightedFeature:
    def __init__(self, feature: Identifiable, weight: int):
        self.feature = feature
        self.weight = weight

    @staticmethod
    def from_dict(data: list) -> Self:
        return WeightedFeature(*data)

    def jsonify(self) -> list:
        data = [self.feature, self.weight]
        return data


@feature_type
@behavior_pack
class WeightedRandomFeature(Feature):
    """
    Represents a data-driven [Weighted Random Feature](https://bedrock.dev/docs/stable/Features#minecraft%3Aweighted_random_feature).
    """

    id = Identifier("weighted_random_feature")
    FILEPATH = "features/weighted_random_feature.json"

    def __init__(self, identifier: Identifiable, features: list[WeightedFeature] = []):
        Feature.__init__(self, identifier)
        self.features = features

    @property
    def features(self) -> list[WeightedFeature]:
        return getattr(self, "_features")

    @features.setter
    def features(self, value: list[WeightedFeature]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_features", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = WeightedRandomFeatureLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["features"] = [x.jsonify() for x in self.features]
        return data

    def get_feature(self, index: int) -> WeightedFeature:
        return self.features[index]

    def add_feature(self, feature: WeightedFeature) -> WeightedFeature:
        if not isinstance(feature, WeightedFeature):
            raise TypeError(
                f"Expected WeightedFeature but got '{feature.__class__.__name__}' instead"
            )
        self.features.append(feature)
        return feature

    def remove_feature(self, index: int) -> WeightedFeature:
        return self.features.pop(index)

    def clear_festures(self) -> Self:
        self.features.clear()
        return self


class WeightedRandomFeatureLoader(Loader):
    name = "Weighted Random Feature"

    def __init__(self):
        from .schemas import WeightedRandomSchem1

        Loader.__init__(self, WeightedRandomFeature)
        self.add_schema(WeightedRandomSchem1, "1.13.0")
        self.add_schema(WeightedRandomSchem1, "1.16.0")
