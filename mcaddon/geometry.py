import os
from typing import Self
from molang import Molang
from dataclasses import dataclass, field
from PIL import Image, ImageFile
import numpy as np

from . import __file__, VERSION
from .file import JsonFile, Loader
from .pack import resource_pack
from .util import (
    getattr2,
    getitem,
    additem,
    removeitem,
    clearitems,
    Identifier,
    Identifiable,
)
from .math import Vector3, Vector2


class Model(Identifiable):
    def __init__(
        self,
        identifier: Identifiable,
    ):
        Identifiable.__init__(self, identifier)

    def __str__(self) -> str:
        return self.__class__.__name__ + "{" + str(self.identifier.path) + "}"

    @staticmethod
    def get_data(vertices, indices) -> np.ndarray:
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vertex_data(self) -> np.ndarray:
        raise NotImplementedError()

    def get_matrix(self):
        raise NotImplementedError()

    def thumbnail(self) -> ImageFile.ImageFile:
        from .ext.mgl import MGLRenderer

        renderer = MGLRenderer().render(self)
        pixels = renderer.fbo.read(components=3, alignment=1)
        return Image.frombytes("RGB", renderer.fbo.size, pixels).transpose(
            Image.FLIP_TOP_BOTTOM
        )

    def geometry(self):
        geo = Geometry(self.identifier)
        geo.add_model(self)
        return geo


# Add support for rendering as an image and support for common 3D libraries like pygame, OpenGL, etc
@resource_pack
class Geometry(JsonFile, Identifiable):

    id = Identifier("geometry")
    FILEPATH = "models/geometry.geo.json"

    def __init__(
        self, identifier: Identifiable, models: dict[Identifiable, Model] = {}
    ):
        Identifiable.__init__(self, identifier)
        self.models = models

    def __str__(self) -> str:
        return "Geometry{" + repr(self.identifier.path) + "}"

    def __iter__(self):
        for i in self.models:
            yield i

    def __getitem__(self, id: Identifiable):
        return self.models[Identifiable.of(id)]

    @property
    def models(self) -> dict[Identifier, Model]:
        return getattr2(self, "_models", {})

    @models.setter
    def models(self, value: dict[Identifiable, Model]):
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        models = {}
        for k, v in value.items():
            models[Identifiable.of(k)] = v
        self.on_update("models", models)
        setattr(self, "_models", models)

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = GeometryLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        data = {"format_version": VERSION["GEOMETRY"], str(self.id): []}
        for v in self.models.values():
            data[str(self.id)].append(v.jsonify())
        return data

    @classmethod
    def open(cls, fp: str, start):
        with open(fp, "r") as fd:
            self = cls.load(fd)
            self.identifier = os.path.relpath(fp, start).replace("\\", "/")
            return self

    # MODEL

    def get_model(self, id: Identifiable) -> Model:
        return getitem(self, "models", Identifiable.of(id))

    def add_model(self, model: Model) -> Model:
        return additem(self, "models", model, model.identifier, Model)

    def remove_model(self, id: Identifiable) -> Model:
        return removeitem(self, "models", Identifiable.of(id))

    def clear_models(self) -> Self:
        """Remove all models"""
        return clearitems(self, "models")


class GeometryLoader(Loader):
    name = "Geometry"

    def __init__(self):
        from .schemas import GeometrySchema1

        Loader.__init__(self, Geometry)
        self.add_schema(GeometrySchema1, "1.12.0")
        self.add_schema(GeometrySchema1, "1.16.0")


@dataclass
class TextureMesh:
    position: Vector3
    rotation: Vector3
    texture: str
    local_pivot: Vector3 = None

    @staticmethod
    def from_dict(data: dict) -> Self:
        position = Vector3.of(data.pop("position"))
        rotation = Vector3.of(data.pop("rotation"))
        texture = data.pop("texture")
        self = TextureMesh(position, rotation, texture)
        if "local_pivot" in data:
            self.local_pivot = Vector3.of(data.pop("local_pivot"))
        return self

    def jsonify(self) -> dict:
        data = {
            "position": self.position.jsonify(),
            "rotation": self.rotation.jsonify(),
            "texture": self.texture,
        }
        if self.local_pivot is not None:
            data["local_pivot"] = self.local_pivot.jsonify()
        return data


@dataclass
class UV:
    uv: Vector2
    uv_size: Vector2 = None

    @staticmethod
    def from_dict(data: dict) -> Self:
        uv = Vector2.of(data.pop("uv"))
        self = UV(uv)
        if "uv_size" in data:
            self.uv_size = Vector2.of(data.pop("uv_size"))
        return self

    def jsonify(self) -> dict:
        data = {"uv": self.uv.jsonify()}
        if self.uv_size is not None:
            data["uv_size"] = self.uv_size.jsonify()
        return data


@dataclass
class Cube:
    origin: Vector3
    size: Vector3
    uv: Vector2 | dict[str, UV] = None
    mirror: bool = False
    inflate: float = None
    rotation: Vector3 = None
    pivot: Vector3 = None

    @staticmethod
    def from_dict(data: dict) -> Self:
        origin = Vector3.of(data.pop("origin"))
        size = Vector3.of(data.pop("size"))
        self = Cube(origin, size)
        if "uv" in data:
            uv = data.pop("uv")
            if isinstance(uv, list):
                self.uv = Vector2.of(uv)
            else:
                uvs = {}
                for k, v in uv.items():
                    uvs[k] = UV.from_dict(v)
                self.uv = uvs
        if "mirror" in data:
            self.mirror = data.pop("mirror")
        if "inflate" in data:
            self.inflate = data.pop("inflate")
        if "rotation" in data:
            self.rotation = Vector3.of(data.pop("rotation"))
        if "pivot" in data:
            self.pivot = Vector3.of(data.pop("pivot"))
        return self

    def jsonify(self) -> dict:
        data = {"origin": self.origin.jsonify(), "size": self.size.jsonify()}
        if self.uv is not None:
            if isinstance(self.uv, dict):
                data["uv"] = {}
                for k, v in self.uv.items():
                    data["uv"][k] = v.jsonify()
            else:
                data["uv"] = self.uv.jsonify()
        if self.mirror:
            data["mirror"] = self.mirror
        if self.inflate:
            data["inflate"] = self.inflate
        if self.rotation is not None:
            data["rotation"] = self.rotation.jsonify()
        if self.pivot is not None:
            data["pivot"] = self.pivot.jsonify()
        return data

    @staticmethod
    def default():
        uv = {
            "north": UV(Vector2(0, 0), Vector2(64, 64)),
            "south": UV(Vector2(0, 0), Vector2(64, 64)),
            "east": UV(Vector2(0, 0), Vector2(64, 64)),
            "west": UV(Vector2(0, 0), Vector2(64, 64)),
            "up": UV(Vector2(64, 64), Vector2(-64, -64)),
            "down": UV(Vector2(64, 64), Vector2(-64, -64)),
        }
        return Cube(Vector3(-8, 0, -8), Vector3(16, 16, 16), uv)


@dataclass
class Bone:
    name: str
    parent: str = None
    mirror: bool = False
    binding: Molang = None
    rotation: Vector3 = None
    texture_meshes: list[TextureMesh] = field(default_factory=list)
    locators: dict[str, Vector3] = field(default_factory=dict)
    pivot: Vector3 = None
    inflate: float = None
    reset: bool = False
    cubes: list[Cube] = field(default_factory=list)

    def __iter__(self):
        for c in self.cubes:
            yield c

    @staticmethod
    def from_dict(data: dict) -> Self:
        name = data.pop("name")
        self = Bone(name)
        if "parent" in data:
            self.parent = data.pop("parent")
        if "mirror" in data:
            self.mirror = data.pop("mirror")
        if "binding" in data:
            self.binding = Molang(data.pop("binding"))
        if "rotation" in data:
            self.rotation = Vector3.of(data.pop("rotation"))
        if "texture_meshes" in data:
            self.texture_meshes = [
                TextureMesh.from_dict(x) for x in data.pop("texture_meshes")
            ]
        if "locators" in data:
            locators = {}
            for k, v in data.pop("locators").items():
                locators[k] = Vector3.of(v)
            self.locators = locators
        if "pivot" in data:
            self.pivot = Vector3.of(data.pop("pivot"))
        if "inflate" in data:
            self.inflate = data.pop("inflate")
        if "reset" in data:
            self.reset = data.pop("reset")
        if "cubes" in data:
            self.cubes = [Cube.from_dict(x) for x in data.pop("cubes")]
        return self

    @staticmethod
    def cube(name: str):
        return Bone(name, cubes=[Cube.default()])

    def jsonify(self) -> dict:
        data = {"name": self.name}
        if self.parent:
            data["parent"] = self.parent
        if self.mirror:
            data["mirror"] = self.mirror
        if self.binding:
            data["binding"] = str(self.binding)
        if self.rotation is not None:
            data["rotation"] = self.rotation.jsonify()
        if self.texture_meshes:
            data["texture_meshes"] = [x.jsonify() for x in self.texture_meshes]
        if self.locators:
            locators = {}
            for k, v in self.locators.items():
                locators[k] = v.jsonify()
            data["locators"] = locators
        if self.pivot is not None:
            data["pivot"] = self.pivot.jsonify()
        if self.inflate:
            data["inflate"] = self.inflate
        if self.reset:
            data["reset"] = self.reset
        if self.cubes:
            data["cubes"] = [x.jsonify() for x in self.cubes]
        return data

    # CUBE

    def get_cube(self, index: int) -> Cube:
        return self.cubes[index]

    def add_cube(self, cube: Cube) -> Cube:
        self.cubes.append(cube)
        return cube

    def remove_cube(self, index) -> Cube:
        return self.cubes.pop(index)

    def clear_cubes(self) -> Self:
        self.cubes.clear()
        return self


class EntityModel(Model):

    id = Identifier("entity")

    def __init__(
        self,
        identifier: Identifiable,
        texture_height: float | int,
        texture_width: float | int,
        visible_bounds_width: float | int = None,
        visible_bounds_height: float | int = None,
        visible_bounds_offset: Vector3 = None,
        bones: dict[str, Bone] = {},
    ):
        Model.__init__(self, identifier)
        self.texture_height = texture_height
        self.texture_width = texture_width
        self.visible_bounds_offset = visible_bounds_offset
        self.visible_bounds_width = visible_bounds_width
        self.visible_bounds_height = visible_bounds_height
        self.bones = bones

    def __iter__(self):
        for bone in self.bones.values():
            yield bone

    def __getitem__(self, name: str):
        return self.bones[name]

    @property
    def texture_width(self) -> float:
        return getattr(self, "_texture_width")

    @texture_width.setter
    def texture_width(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("texture_width", v)
        setattr(self, "_texture_width", v)

    @property
    def texture_height(self) -> float:
        return getattr(self, "_texture_height")

    @texture_height.setter
    def texture_height(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("texture_height", v)
        setattr(self, "_texture_height", v)

    @property
    def visible_bounds_offset(self) -> Vector3:
        return getattr(self, "_visible_bounds_offset", None)

    @visible_bounds_offset.setter
    def visible_bounds_offset(self, value: Vector3):
        if value is None:
            return
        elif isinstance(value, (float, int)):
            self.visible_bounds_offset = Vector3(value, value, value)
        elif isinstance(value, Vector3):
            self.on_update("visible_bounds_offset", value)
            setattr(self, "_visible_bounds_offset", value)
        else:
            raise TypeError(
                f"Expected Vector3 but got '{value.__class__.__name__}' instead"
            )

    @property
    def visable_bounds_width(self) -> float:
        return getattr(self, "_visable_bounds_width")

    @visable_bounds_width.setter
    def visable_bounds_width(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("visable_bounds_width", v)
        setattr(self, "_visable_bounds_width", v)

    @property
    def visable_bounds_height(self) -> float:
        return getattr(self, "_visable_bounds_height")

    @visable_bounds_height.setter
    def visable_bounds_height(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("visable_bounds_height", v)
        setattr(self, "_visable_bounds_height", v)

    @property
    def bone(self) -> dict[str, Bone]:
        return getattr(self, "_bone", {})

    @bone.setter
    def bone(self, value: dict[str, Bone]):
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        self.on_update("bone", value)
        setattr(self, "_bone", value)

    @staticmethod
    def from_dict(data: dict) -> Self:
        desc = data.pop("description")
        id = desc["identifier"]
        texture_height = desc.get("texture_height")
        texture_width = desc.get("texture_width")
        visible_bounds_offset = desc.get("visible_bounds_offset")
        visible_bounds_width = desc.get("visible_bounds_width")
        visible_bounds_height = desc.get("visible_bounds_height")
        bones = {}
        for x in data.pop("bones"):
            b = Bone.from_dict(x)
            bones[b.name] = b

        return EntityModel(
            id,
            texture_height,
            texture_width,
            visible_bounds_offset,
            visible_bounds_width,
            visible_bounds_height,
            bones,
        )

    @staticmethod
    def cube(id: Identifiable):
        model = EntityModel(id, 64, 64, 2, 2.5, Vector3(0, 0.75, 0))
        model.add_bone(Bone.cube(model.identifier.path))
        return model

    def jsonify(self) -> dict:
        data = {
            "description": {"identifier": str(self.identifier)},
            "bones": [bone.jsonify() for bone in self.bones.values()],
        }
        if self.texture_height:
            data["description"]["texture_height"] = self.texture_height
        if self.texture_width:
            data["description"]["texture_width"] = self.texture_width
        if self.visible_bounds_width:
            data["description"]["visible_bounds_width"] = self.visible_bounds_width
        if self.visible_bounds_height:
            data["description"]["visible_bounds_height"] = self.visible_bounds_height
        if self.visible_bounds_offset is not None:
            data["description"][
                "visible_bounds_offset"
            ] = self.visible_bounds_offset.jsonify()
        return data

    def get_vertex_data(self) -> np.ndarray:
        # Should get vertex data for all self.bones.cubes
        vertices = [
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
        ]
        indices = [
            (0, 2, 3),
            (0, 1, 2),
            (1, 7, 2),
            (1, 6, 7),
            (6, 5, 4),
            (4, 7, 6),
            (3, 4, 5),
            (3, 5, 0),
            (3, 7, 4),
            (3, 2, 7),
            (0, 6, 1),
            (0, 5, 6),
        ]

        vertex_data = self.get_data(vertices, indices)

        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 1, 2),
            (2, 3, 0),
            (2, 3, 0),
            (2, 0, 1),
            (0, 2, 3),
            (0, 1, 2),
            (3, 1, 2),
            (3, 0, 1),
        ]
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        normals = [
            (0, 0, 1) * 6,
            (1, 0, 0) * 6,
            (0, 0, -1) * 6,
            (-1, 0, 0) * 6,
            (0, 1, 0) * 6,
            (0, -1, 0) * 6,
        ]
        normals = np.array(normals, dtype="f4").reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data

    def get_matrix(self):
        import glm  # PyGLM

        pos = (0, 0, -10)
        rot = glm.vec3([glm.radians(a) for a in (0, 0, 0)])
        scale = (1, 1, 1)
        m_model = glm.mat4()
        # Translate
        m_model = glm.translate(m_model, pos)
        # Rotate
        m_model = glm.rotate(m_model, rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, rot.z, glm.vec3(0, 0, 1))
        # Scale
        m_model = glm.scale(m_model, scale)
        return m_model

    # BONES
    def get_bone(self, name: str) -> Bone:
        return getitem(self, "bones", name)

    def add_bone(self, bone: Bone) -> Bone:
        return additem(self, "bones", bone, bone.name, Bone)

    def remove_bone(self, name) -> Bone:
        return removeitem(self, "bones", name)

    def clear_bones(self) -> Self:
        """Remove all bones"""
        return clearitems(self, "bones")
