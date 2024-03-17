from typing import Self

from . import VERSION

from .util import (
    Identifiable,
    Identifier,
    Misc,
    setattr2,
    getattr2,
    getitem,
    additem,
    removeitem,
    clearitems,
)
from .constant import Direction
from .file import JsonFile, Loader
from .pack import resource_pack


class GeometryPart(Misc):
    def __init__(self, bone: str, cube: int = None, face: Direction = None):
        self.bone = bone
        self.cube = cube
        self.face = face

    @property
    def bone(self) -> str:
        return getattr(self, "_bone")

    @bone.setter
    def bone(self, value: str):
        setattr(self, "_bone", str(value))

    @property
    def cube(self) -> int:
        return getattr(self, "_cube", None)

    @cube.setter
    def cube(self, value: int):
        if value is None:
            return
        setattr2(self, "_cube", value, int)

    @property
    def face(self) -> Direction:
        return getattr(self, "_face", None)

    @face.setter
    def face(self, value: Direction):
        if value is None:
            return
        setattr2(self, "_face", value, Direction)

    @staticmethod
    def from_dict(data: dict) -> Self:
        bone = data.pop("bone") if "bone" in data else None
        cube = data.pop("cube") if "cube" in data else None
        face = Direction.from_dict(data.pop("face")) if "face" in data else None
        return GeometryPart(bone, cube, face)

    def jsonify(self) -> dict:
        data = {}
        if self.bone:
            data["bone"] = self.bone
        if self.cube is not None:
            data["cube"] = self.cube
        if self.face:
            data["face"] = Direction.jsonify(self.face)
        return data


class CullingRule(Misc):
    def __init__(self, direction: str, geometry_part: GeometryPart):
        self.direction = direction
        self.geometry_part = geometry_part

    @property
    def direction(self) -> Direction:
        """Specifies the direction of the neighbor block to check for culling. This direction rotates with a block's Transform component."""
        return getattr(self, "_direction")

    @direction.setter
    def direction(self, value: Direction):
        if not isinstance(value, Direction):
            raise TypeError(
                f"Expected Direction but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_direction", value)

    @property
    def geometry_part(self) -> GeometryPart:
        """Specifies the bone, cube, and face that the block will be culled. The cube and face fields are optional to allow culling a specific face. Omitting these fields will cull the whole bone."""
        return getattr(self, "_geometry_part")

    @geometry_part.setter
    def geometry_part(self, value: GeometryPart):
        if not isinstance(value, GeometryPart):
            raise TypeError(
                f"Expected GeometryPart but got '{value.__class__.__name__}' instead"
            )
        self.on_update("geometry_part", value)
        setattr(self, "_geometry_part", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        direction = Direction.from_dict(data.pop("direction"))
        geometry_part = GeometryPart.from_dict(data.pop("geometry_part"))
        return CullingRule(direction, geometry_part)

    def jsonify(self) -> dict:
        data = {
            "geometry_part": self.geometry_part.jsonify(),
            "direction": self.direction.jsonify(),
        }
        return data


@resource_pack
class BlockCullingRules(JsonFile, Identifiable):

    id = Identifier("block_culling_rules")
    FILEPATH = "block_culling/block_culling.json"

    def __init__(self, identifier: Identifiable, rules: list[CullingRule] = None):
        Identifiable.__init__(self, identifier)
        self.rules = rules

    @property
    def rules(self) -> list[CullingRule]:
        """List of all components used to identify geometry parts used in culling."""
        return getattr2(self, "_rules", [])

    @rules.setter
    def rules(self, value: list[CullingRule]):
        self.on_update("rules", value)
        setattr2(self, "_rules", value, list)

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = BlockCullingRulesLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        cull = {"rules": [x.jsonify() for x in self.rules]}
        root = str(self.id)
        data = {
            "format_version": VERSION["BLOCK_CULLING_RULES"],
            root: {"description": {"identifier": str(self.identifier)}},
        }
        for k, v in cull.items():
            data[root][k] = v
        return data

    def get_rule(self, index: int) -> CullingRule:
        return getitem(self, "rules", index)

    def add_rule(self, rule: CullingRule) -> CullingRule:
        return additem(self, "rules", rule, type=CullingRule)

    def add_rules(self, *rule: CullingRule) -> list[CullingRule]:
        return [self.add_rule(rule) for rule in rule]

    def remove_rule(self, index: int) -> CullingRule:
        return removeitem(self, "rules", index)

    def clear_rules(self) -> Self:
        """Remove all rules"""
        return clearitems(self, "rules")


class BlockCullingRulesLoader(Loader):
    name = "Block Culling Rules"

    def __init__(self):
        from .schemas import BlockCullingRulesSchema1

        Loader.__init__(self, BlockCullingRules)
        self.add_schema(BlockCullingRulesSchema1, "1.20.60")
