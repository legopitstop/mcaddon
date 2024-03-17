# TODO: https://bedrock.dev/docs/stable/Features#Feature%20rule%20schema
from typing import Self
from molang import Molang

from . import VERSION
from .feature import DistributionProvider
from .predicate import Filters
from .pack import behavior_pack
from .util import Misc, Identifier, Identifiable
from .file import JsonFile, Loader


class Distribution:
    id = Identifier("scatter_feature")
    FILEPATH = "features/scatter_feature.json"

    def __init__(
        self,
        iterations: Molang,
        x: DistributionProvider | int,
        y: DistributionProvider | int,
        z: DistributionProvider | int,
        scatter_chance: float = None,
    ):
        self.iterations = iterations
        self.x = x
        self.y = y
        self.z = z
        self.scatter_chance = scatter_chance

    @property
    def z(self) -> DistributionProvider | int:
        return getattr(self, "_z")

    @z.setter
    def z(self, value: DistributionProvider | int):
        if not isinstance(value, (DistributionProvider, int)):
            raise TypeError(
                f"Expected DistributionProvider, int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_z", value)

    @property
    def y(self) -> DistributionProvider | int:
        return getattr(self, "_y")

    @y.setter
    def y(self, value: DistributionProvider | int):
        if not isinstance(value, (DistributionProvider, int)):
            raise TypeError(
                f"Expected DistributionProvider, int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_y", value)

    @property
    def x(self) -> DistributionProvider | int:
        return getattr(self, "_x")

    @x.setter
    def x(self, value: DistributionProvider | int):
        if not isinstance(value, (DistributionProvider, int)):
            raise TypeError(
                f"Expected DistributionProvider, int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_x", value)

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

    @staticmethod
    def from_dict(data: dict) -> Self:
        scatter_chance = (
            data.pop("scatter_chance") if "scatter_chance" in data else None
        )
        iterations = data.pop("iterations")
        x = DistributionProvider.from_dict(data.pop("x"))
        y = DistributionProvider.from_dict(data.pop("y"))
        z = DistributionProvider.from_dict(data.pop("z"))
        return Distribution(iterations, x, y, z, scatter_chance)

    def jsonify(self) -> dict:
        data = {"iterations": self.iterations}
        if self.scatter_chance:
            data["scatter_chance"] = self.scatter_chance
        data["x"] = (
            self.x.jsonify() if isinstance(self.x, DistributionProvider) else self.x
        )
        data["y"] = (
            self.y.jsonify() if isinstance(self.y, DistributionProvider) else self.y
        )
        data["z"] = (
            self.z.jsonify() if isinstance(self.z, DistributionProvider) else self.z
        )
        return data


class FeatureRuleCondition(Misc):
    def __init__(self, placement_pass: str, biome_filter: Filters):
        self.placement_pass = placement_pass
        self.biome_filter = biome_filter

    @property
    def placement_pass(self) -> str:
        return getattr(self, "_placement_pass")

    @placement_pass.setter
    def placement_pass(self, value: str):
        setattr(self, "_placement_pass", str(value))

    @property
    def biome_filter(self) -> Filters:
        return getattr(self, "_biome_filter")

    @biome_filter.setter
    def biome_filter(self, value: Filters):
        if not isinstance(value, Filters):
            raise TypeError(
                f"Expected Filters but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_biome_filter", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        placement_pass = data.pop("placement_pass")
        biome_filter = Filters.from_dict(data.pop("minecraft:biome_filter"))
        return FeatureRuleCondition(placement_pass, biome_filter)

    def jsonify(self) -> dict:
        data = {
            "placement_pass": self.placement_pass,
            "minecraft:biome_filter": self.biome_filter.jsonify(),
        }
        return data


@behavior_pack
class FeatureRule(JsonFile, Identifiable):
    id = Identifier("feature_rules")
    FILEPATH = "feature_rules/feature_rule.json"

    def __init__(
        self,
        identifier: Identifiable,
        places_feature: Identifiable,
        conditions: FeatureRuleCondition,
        distribution: Distribution,
    ):
        Identifiable.__init__(self, identifier)
        self.places_feature = places_feature
        self.conditions = conditions
        self.distribution = distribution

    def __str__(self) -> str:
        return "FeatureRule{" + str(self.identifier) + "}"

    @property
    def places_feature(self) -> Identifier:
        return getattr(self, "_places_feature")

    @places_feature.setter
    def places_feature(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("places_feature", id)
        setattr(self, "_places_feature", id)

    @property
    def conditions(self) -> FeatureRuleCondition:
        return getattr(self, "_conditions")

    @conditions.setter
    def conditions(self, value: FeatureRuleCondition):
        if not isinstance(value, FeatureRuleCondition):
            raise TypeError(
                f"Expected FeatureRuleCondition but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_conditions", value)

    @property
    def distribution(self) -> Distribution:
        return getattr(self, "_distribution")

    @distribution.setter
    def distribution(self, value: Distribution):
        if not isinstance(value, Distribution):
            raise TypeError(
                f"Expected Distribution but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_distribution", value)

    def jsonify(self) -> dict:
        feature_rule = {
            "conditions": self.conditions.jsonify(),
            "distribution": self.distribution.jsonify(),
        }
        data = {
            "format_version": VERSION["FEATURE_RULE"],
            str(self.id): {
                "description": {
                    "identifier": str(self.identifier),
                    "places_feature": str(self.places_feature),
                }
            },
        }
        for k, v in feature_rule.items():
            data[str(self.id)][k] = v
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = FeatureRuleLoader()
        loader.validate(data)
        return loader.load(data)


class FeatureRuleLoader(Loader):
    name = "Feature Rule"

    def __init__(self):
        from .schemas import FeatureRuleSchem1

        Loader.__init__(self, FeatureRule)
        self.add_schema(FeatureRuleSchem1, "1.12")
