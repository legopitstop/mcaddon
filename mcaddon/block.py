from typing import Self
from molang import Molang
from dataclasses import dataclass

from . import VERSION
from .item import ItemStack
from .registry import INSTANCE, Registries
from .exception import ComponentNotFoundError
from .constant import RenderMethod, BlockFace
from .file import JsonFile, Loader
from .util import getattr2, stringify, Box, Identifier, MenuCategory, Identifiable
from .state import (
    BlockState,
    CardinalDirectionState,
    FacingDirectionState,
    BlockFaceState,
    VerticalHalfState,
)
from .event import *


class BlockComponent:
    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return "BlockComponent{" + str(self.id) + "}"

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        raise NotImplementedError()


class SimpleBlockComponent(BlockComponent):
    def __init__(self, value):
        self.value = value

    @property
    def __dict__(self):
        data = self.value
        return data

    @classmethod
    def from_dict(cls, data) -> Self:
        self = cls.__new__(cls)
        self.value = data
        return self

    @property
    def value(self):
        return getattr(self, "_value")

    @value.setter
    def value(self, value):
        if not isinstance(value, self.clazz):
            raise TypeError(
                f"Expected {self.clazz.__name__} but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_value", value)


# COMPONENTS

INSTANCE.create_registry(Registries.BLOCK_COMPONENT_TYPE, BlockComponent)


def block_component_type(cls):
    """
    Add this block component to the registry
    """

    def wrapper():
        return INSTANCE.register(Registries.BLOCK_COMPONENT_TYPE, cls.id, cls)

    return wrapper()


@block_component_type
class OnFallOnComponent(Trigger, BlockComponent):
    """Describes event for this block."""

    id = Identifier("on_fall_on")

    def __init__(
        self,
        event: str = "on_fall_on",
        min_fall_distance: float = 0.0,
        condition: str = None,
        target: str = None,
    ):
        Trigger.__init__(self, event, condition, target)
        self.min_fall_distance = min_fall_distance

    @property
    def __dict__(self):
        data = super().__dict__
        if self.min_fall_distance is not None:
            data["min_fall_distance"] = self.min_fall_distance
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        if "min_fall_distance" in data:
            self.min_fall_distance = data.pop("min_fall_distance")
        return self

    @property
    def min_fall_distance(self) -> float:
        """The event executed on the block, defaults to 'on_fall_on'"""
        return getattr(self, "_min_fall_distance", None)

    @min_fall_distance.setter
    def min_fall_distance(self, value: float):
        if value is None:
            setattr(self, "_min_fall_distance", None)
            return
        setattr(self, "_min_fall_distance", float(value))


@block_component_type
class OnInteractComponent(Trigger, BlockComponent):
    """Describes event for this block."""

    id = Identifier("on_interact")

    def __init__(
        self, event: str = "on_interact", condition: str = None, target: str = None
    ):
        Trigger.__init__(self, event, condition, target)


@block_component_type
class OnPlacedComponent(Trigger, BlockComponent):
    """Describes event for this block."""

    id = Identifier("on_placed")

    def __init__(
        self, event: str = "on_placed", condition: str = None, target: str = None
    ):
        Trigger.__init__(self, event, condition, target)


@block_component_type
class OnPlayerDestroyedComponent(Trigger, BlockComponent):
    """Describes event for this block."""

    id = Identifier("on_player_destroyed")

    def __init__(
        self,
        event: str = "on_player_destroyed",
        condition: str = None,
        target: str = None,
    ):
        Trigger.__init__(self, event, condition, target)


@block_component_type
class OnPlayerPlacingComponent(Trigger, BlockComponent):
    """Describes event for this block."""

    id = Identifier("on_player_placing")

    def __init__(
        self,
        event: str = "on_player_placing",
        condition: str = None,
        target: str = None,
    ):
        Trigger.__init__(self, event, condition, target)


@block_component_type
class OnStepOffComponent(Trigger, BlockComponent):
    """Describes event for this block."""

    id = Identifier("on_step_off")

    def __init__(
        self, event: str = "on_step_off", condition: str = None, target: str = None
    ):
        Trigger.__init__(self, event, condition, target)


@block_component_type
class OnStepOnComponent(Trigger, BlockComponent):
    """Describes event for this block."""

    id = Identifier("on_step_on")

    def __init__(
        self, event: str = "on_step_on", condition: str = None, target: str = None
    ):
        Trigger.__init__(self, event, condition, target)


@block_component_type
class BoneVisabilityComponent(BlockComponent):
    """Tells whether the bone should be visible or not (value)."""

    id = Identifier("bone_visability")

    def __init__(self, bones: dict[str, Molang | bool] = None):
        self.bones = bones

    @property
    def __dict__(self) -> dict:
        data = {"bones": {}}
        for k, v in self.bones.items():
            data["bones"][k] = str(v)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.bones = data.pop("bones")
        return self

    @property
    def bones(self) -> dict[str, Molang | bool]:
        return getattr2(self, "_bones", {})

    @bones.setter
    def bones(self, value: dict[str, Molang | bool]):
        if value is None:
            self.bones = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict[str, Molang|bool] but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_bones", value)

    def get_bone(self, bone: str) -> Molang | None:
        return self.bones.get(bone)

    def add_bone(self, bone: str, condition: Molang) -> Molang:
        self.bones[bone] = Molang(condition)
        return condition

    def remove_bone(self, bone: str) -> Molang:
        return self.bones.pop(bone)

    def clear_bones(self) -> Self:
        self.bones = {}
        return self


@block_component_type
class BreathabilityComponent(SimpleBlockComponent):
    id = Identifier("breathability")
    clazz = str


@block_component_type
class CollisionBoxComponent(BlockComponent, Box):
    """Defines the area of the block that collides with entities. If set to true, default values are used. If set to false, the block's collision with entities is disabled. If this component is omitted, default values are used."""

    id = Identifier("collision_box")

    def __init__(self, origin: list | bool = None, size: list = None):
        if isinstance(origin, bool):
            if origin:
                origin = [-8, 0, -8]
                size = [16, 16, 16]
            else:
                origin = [0, 0, 0]
                size = [0, 0, 0]
        Box.__init__(self, origin, size)

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        if self.is_cube():
            return True
        elif self.is_none():
            return False
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if isinstance(data, bool):
            return cls.cube() if data else cls.none()
        if "origin" in data:
            self.origin = data.pop("origin")
        if "size" in data:
            self.size = data.pop("size")
        return self


@block_component_type
class SelectionBoxComponent(BlockComponent, Box):
    """Defines the area of the block that is selected by the player's cursor. If set to true, default values are used. If set to false, this block is not selectable by the player's cursor. If this component is omitted, default values are used."""

    id = Identifier("selection_box")

    def __init__(self, origin: list | bool = None, size: list = None):
        if isinstance(origin, bool):
            if origin:
                origin = [-8, 0, -8]
                size = [16, 16, 16]
            else:
                origin = [0, 0, 0]
                size = [0, 0, 0]
        Box.__init__(self, origin, size)

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        if self.is_cube():
            return True
        elif self.is_none():
            return False
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if isinstance(data, bool):
            return cls.cube() if data else cls.none()
        if "origin" in data:
            self.origin = data.pop("origin")
        if "size" in data:
            self.size = data.pop("size")
        return self


@block_component_type
class CraftingTableComponent(BlockComponent):
    """Makes your block into a custom crafting table which enables the crafting table UI and the ability to craft recipes. This component supports only "recipe_shaped" and "recipe_shapeless" typed recipes and not others like "recipe_furnace" or "recipe_brewing_mix". If there are two recipes for one item, the recipe book will pick the first that was parsed. If two input recipes are the same, crafting may assert and the resulting item may vary."""

    id = Identifier("crafting_table")

    def __init__(self, table_name: str, crafting_tags: list[str] = []):
        self.table_name = table_name
        self.crafting_tags = crafting_tags

    @property
    def __dict__(self) -> dict:
        data = {"crafting_tags": self.crafting_tags, "table_name": self.table_name}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.crafting_tags = data.pop("crafting_tags")
        self.table_name = data.pop("table_name")
        return self

    @property
    def crafting_tags(self) -> list[str]:
        """Defines the tags recipes should define to be crafted on this table. Limited to 64 tags. Each tag is limited to 64 characters."""
        return getattr2(self, "_crafting_tags", ["crafting_table"])

    @crafting_tags.setter
    def crafting_tags(self, value: list[str]):
        if value is None:
            self.crafting_tags = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list[str] but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_crafting_tags", value)

    @property
    def table_name(self) -> str:
        """Specifies the language file key that maps to what text will be displayed in the UI of this table. If the string given can not be resolved as a loc string, the raw string given will be displayed. If this field is omitted, the name displayed will default to the name specified in the "display_name" component. If this block has no "display_name" component, the name displayed will default to the name of the block."""
        return getattr(self, "_table_name")

    @table_name.setter
    def table_name(self, value: str):
        setattr(self, "_table_name", str(value))

    def get_crafting_tag(self, index: int) -> str | None:
        return self.crafting_tags[index]

    def add_crafting_tag(self, tag: str) -> str:
        self.crafting_tags.append(tag)
        return tag

    def remove_crafting_tag(self, index: int) -> str:
        return self.crafting_tags.pop(index)

    def clear_crafting_tags(self) -> Self:
        self.crafting_tags = []
        return self


@block_component_type
class DestructibleByExplosionComponent(BlockComponent):
    """Describes the destructible by explosion properties for this block. If set to true, the block will have the default explosion resistance. If set to false, this block is indestructible by explosion. If the component is omitted, the block will have the default explosion resistance"""

    id = Identifier("destructible_by_explosion")

    def __init__(self, explosion_resistance: float = None):
        self.explosion_resistance = explosion_resistance

    @property
    def __dict__(self) -> dict:
        data = {}
        if self.explosion_resistance is not None:
            data["explosion_resistance"] = self.explosion_resistance
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "explosion_resistance" in data:
            self.explosion_resistance = data.pop("explosion_resistance")
        return self

    @property
    def explosion_resistance(self) -> float:
        """Sets the explosion resistance for the block. Greater values result in greater resistance to explosions. The scale will be different for different explosion power levels. A negative value or 0 means it will easily explode; larger numbers increase level of resistance."""
        return getattr(self, "_explosion_resistance")

    @explosion_resistance.setter
    def explosion_resistance(self, value: float):
        if value is None:
            setattr(self, "_explosion_resistance", value)
            return
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_explosion_resistance", value)


@block_component_type
class DestructibleByMiningComponent(BlockComponent):
    """Describes the destructible by mining properties for this block. If set to true, the block will take the default number of seconds to destroy. If set to false, this block is indestructible by mining. If the component is omitted, the block will take the default number of seconds to destroy."""

    id = Identifier("destructible_by_mining")

    def __init__(self, seconds_to_destroy: float = None):
        self.seconds_to_destroy = seconds_to_destroy

    @property
    def __dict__(self) -> dict:
        data = {}
        if self.seconds_to_destroy is not None:
            data["seconds_to_destroy"] = self.seconds_to_destroy
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "seconds_to_destroy" in data:
            self.seconds_to_destroy = data.pop("seconds_to_destroy")
        return self

    @property
    def seconds_to_destroy(self) -> float:
        """Sets the number of seconds it takes to destroy the block with base equipment. Greater numbers result in greater mining times."""
        return getattr(self, "_seconds_to_destroy", None)

    @seconds_to_destroy.setter
    def seconds_to_destroy(self, value: float):
        if value is None:
            setattr(self, "_seconds_to_destroy", None)
            return
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float or int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_seconds_to_destroy", value)


@block_component_type
class BlockDisplayNameComponent(SimpleBlockComponent):
    """Specifies the language file key that maps to what text will be displayed when you hover over the block in your inventory and hotbar. If the string given can not be resolved as a loc string, the raw string given will be displayed. If this component is omitted, the name of the block will be used as the display name."""

    id = Identifier("display_name")
    clazz = str


@block_component_type
class FlammableComponent(BlockComponent):
    """Describes the flammable properties for this block. If set to true, default values are used. If set to false, or if this component is omitted, the block will not be able to catch on fire naturally from neighbors, but it can still be directly ignited."""

    id = Identifier("flammable")

    def __init__(
        self, catch_chance_modifier: int = None, destroy_chance_modifier: int = None
    ):
        self.catch_chance_modifier = catch_chance_modifier
        self.destroy_chance_modifier = destroy_chance_modifier

    @property
    def __dict__(self) -> dict:
        data = {}
        if self.catch_chance_modifier is not None:
            data["catch_chance_modifier"] = self.catch_chance_modifier
        if self.destroy_chance_modifier is not None:
            data["destroy_chance_modifier"] = self.destroy_chance_modifier
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "catch_chance_modifier" in data:
            self.catch_chance_modifier = data.pop("catch_chance_modifier")
        if "destroy_chance_modifier" in data:
            self.destroy_chance_modifier = data.pop("destroy_chance_modifier")
        return self

    @property
    def catch_chance_modifier(self) -> int:
        """A modifier affecting the chance that this block will catch flame when next to a fire. Values are greater than or equal to 0, with a higher number meaning more likely to catch on fire. For a "catch_chance_modifier" greater than 0, the fire will continue to burn until the block is destroyed (or it will burn forever if the "destroy_chance_modifier" is 0). If the "catch_chance_modifier" is 0, and the block is directly ignited, the fire will eventually burn out without destroying the block (or it will have a chance to be destroyed if "destroy_chance_modifier" is greater than 0). The default value of 5 is the same as that of Planks."""
        return getattr(self, "_catch_chance_modifier", None)

    @catch_chance_modifier.setter
    def catch_chance_modifier(self, value: int):
        if value is None:
            setattr(self, "_catch_chance_modifier", None)
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_catch_chance_modifier", value)

    @property
    def destroy_chance_modifier(self) -> int:
        """A modifier affecting the chance that this block will be destroyed by flames when on fire. Values are greater than or equal to 0, with a higher number meaning more likely to be destroyed by fire. For a "destroy_chance_modifier" of 0, the block will never be destroyed by fire, and the fire will burn forever if the "catch_chance_modifier" is greater than 0. The default value of 20 is the same as that of Planks."""
        return getattr(self, "_destroy_chance_modifier", None)

    @destroy_chance_modifier.setter
    def destroy_chance_modifier(self, value: int):
        if value is None:
            setattr(self, "_destroy_chance_modifier", None)
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_destroy_chance_modifier", value)


@block_component_type
class FrictionComponent(BlockComponent):
    """Describes the friction for this block in a range of (0.0-0.9). Friction affects an entity's movement speed when it travels on the block. Greater value results in more friction."""

    id = Identifier("friction")
    clazz = float

    def __init__(self, value: float):
        self.value = value

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.value = data
        return self

    @property
    def __dict__(self) -> int:
        data = 0.4 if self.value is None else self.value
        return data

    @property
    def value(self) -> float:
        return getattr(self, "_value")

    @value.setter
    def value(self, value: float):
        if not isinstance(value, float):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_value", value)


@block_component_type
class GeometryComponent(BlockComponent):
    """The description identifier of the geometry file to use to render this block. This identifier must match an existing geometry identifier in any of the currently loaded resource packs."""

    id = Identifier("geometry")

    def __init__(self, geometry: str, bone_visability: dict[str, Molang | bool] = {}):
        self.geometry = geometry
        self.bone_visability = bone_visability

    @property
    def __dict__(self) -> dict:
        data = {"identifier": self.geometry}
        if self.bone_visability:
            data["bone_visability"] = {}
            for k, v in self.bone_visability.items():
                data["bone_visability"][k] = str(v)
        else:
            return str(self.geometry)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if isinstance(data, str):
            self.geometry = data
        elif isinstance(data, dict):
            self.geometry = data.pop("identifier")
            if "bone_visability" in data:
                self.bone_visability = data.pop("bone_visability")
        return self

    @property
    def geometry(self) -> str:
        return getattr(self, "_geometry")

    @geometry.setter
    def geometry(self, value: str):
        setattr(self, "_geometry", str(value))

    @property
    def bone_visability(self) -> dict[str, Molang | bool]:
        return getattr(self, "_bone_visability", {})

    @bone_visability.setter
    def bone_visability(self, value: dict[str, Molang | bool]):
        if value is None:
            self.bone_visability = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_bone_visability", value)


@block_component_type
class LightDampeningComponent(SimpleBlockComponent):
    """The amount that light will be dampened when it passes through the block, in a range (0-15). Higher value means the light will be dampened more."""

    id = Identifier("light_dampening")
    clazz = int

    @property
    def __dict__(self) -> int:
        data = 15 if self.value is None else self.value
        return data


@block_component_type
class LightEmissionComponent(SimpleBlockComponent):
    """The amount of light this block will emit in a range (0-15). Higher value means more light will be emitted."""

    id = Identifier("light_emission")
    clazz = int

    @property
    def __dict__(self) -> str:
        data = 0 if self.value is None else self.value
        return data


@block_component_type
class LootComponent(SimpleBlockComponent):
    """The path to the loot table, relative to the behavior pack. Path string is limited to 256 characters."""

    id = Identifier("loot")
    clazz = str

    @classmethod
    def empty(cls) -> Self:
        return LootComponent("loot_tables/empty.json")


@block_component_type
class MapColorComponent(SimpleBlockComponent):
    """Sets the color of the block when rendered to a map. The color is represented as a hex value in the format "#RRGGBB". May also be expressed as an array of [R, G, B] from 0 to 255. If this component is omitted, the block will not show up on the map."""

    id = Identifier("map_color")
    clazz = str


class Material:
    """A material instance definition to map to a material instance in a geometry file. The material instance "*" will be used for any materials that don't have a match."""

    def __init__(
        self,
        texture: Identifier,
        render_method: RenderMethod = RenderMethod.opaque,
        ambient_occlusion: bool = True,
        face_dimming: bool = True,
    ):
        self.texture = texture
        self.ambient_occlusion = ambient_occlusion
        self.face_dimming = face_dimming
        self.render_method = render_method

    @property
    def __dict__(self) -> dict:
        data = {"texture": str(self.texture)}
        if self.render_method not in [None, RenderMethod.opaque]:
            data["render_method"] = self.render_method._value_
        if self.ambient_occlusion not in [None, True]:
            data["ambient_occlusion"] = self.ambient_occlusion
        if self.face_dimming not in [None, True]:
            data["face_dimming"] = self.face_dimming
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.texture = data.pop("texture")
        if "ambient_occlusion" in data:
            self.ambient_occlusion = data.pop("ambient_occlusion")
        if "face_dimming" in data:
            self.face_dimming = data.pop("face_dimming")
        if "render_method" in data:
            self.render_method = data.pop("render_method")
        return self

    @property
    def texture(self) -> Identifier:
        """Texture name for the material."""
        return getattr(self, "_texture")

    @texture.setter
    def texture(self, value: Identifier):
        setattr(self, "_texture", Identifier(value))

    @property
    def ambient_occlusion(self) -> bool:
        """Should this material have ambient occlusion applied when lighting? If true, shadows will be created around and underneath the block."""
        return getattr(self, "_ambient_occlusion", None)

    @ambient_occlusion.setter
    def ambient_occlusion(self, value: bool):
        if value is None:
            setattr(self, "_ambient_occlusion", None)
            return
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_ambient_occlusion", value)

    @property
    def face_dimming(self) -> bool:
        """Should this material be dimmed by the direction it's facing?"""
        return getattr(self, "_face_dimming", None)

    @face_dimming.setter
    def face_dimming(self, value: bool):
        if value is None:
            setattr(self, "_face_dimming", None)
            return
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_face_dimming", value)

    @property
    def render_method(self) -> RenderMethod:
        """
        The render method to use. Must be one of these options:

        "opaque" - Used for a regular block texture without an alpha layer. Does not allow for transparency or translucency.

        "double_sided" - Used for completely disabling backface culling.

        "blend" - Used for a block like stained glass. Allows for transparency and translucency (slightly transparent textures).

        "alpha_test" - Used for a block like the vanilla (unstained) glass. Does not allow for translucency, only fully opaque or fully transparent textures. Also disables backface culling.
        """
        return getattr(self, "_render_method", None)

    @render_method.setter
    def render_method(self, value: RenderMethod):
        if value is None:
            setattr(self, "_render_method", None)
            return
        if isinstance(value, RenderMethod):
            setattr(self, "_render_method", value)
        else:
            self.render_method = RenderMethod[str(value)]


@block_component_type
class MaterialInstancesComponent(BlockComponent):
    """The material instances for a block. Maps face or material_instance names in a geometry file to an actual material instance. You can assign a material instance object to any of these faces: "up", "down", "north", "south", "east", "west", or "*". You can also give an instance the name of your choosing such as "my_instance", and then assign it to a face by doing "north":"my_instance"."""

    id = Identifier("material_instances")

    def __init__(self, materials: dict[str, Material] = None):
        self.materials = {}

    @property
    def __dict__(self) -> dict:
        data = {}
        for k, v in self.materials.items():
            data[k] = v.__dict__
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        for k, v in data.items():
            self.materials[k] = Material.from_dict(v)
        return self

    @property
    def materials(self) -> dict[str, Material]:
        return getattr2(self, "_materials", {})

    @materials.setter
    def materials(self, value: dict[str, Material]):
        if value is None:
            setattr(self, "_materials", {})
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict[str, Material] but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_materials", value)

    def get_material(self, instance_name: str) -> Material | None:
        return self.materials.get(instance_name)

    def add_material(self, instance_name: str, material: Material) -> Material:
        if isinstance(instance_name, (list, tuple)):
            for name in instance_name:
                self.add_material(name, material)
            return material
        if not isinstance(material, Material):
            raise TypeError(
                f"Expected Material but got '{material.__class__.__name__}' instead"
            )
        self.materials[str(instance_name)] = material
        return material

    def remove_material(self, instance_name: str) -> Material:
        m = self.materials[str(instance_name)]
        del self.materials[str(instance_name)]
        return m


class BlockDescriptor:
    def __init__(self, name: str = None, states: list = None, tags: str = "1"):
        self.name = name
        self.states = states
        self.tags = tags

    @property
    def __dict__(self) -> dict:
        data = {}
        if self.name:
            data["name"] = str(self.name)
        elif self.tags:
            data["tags"] = self.tags
        if self.states:
            data["states"] = self.states
        if "name" in data and "states" not in data:
            data = data["name"]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.name = data.pop("name")
        self.states = data.pop("states")
        self.tags = data.pop("tags")
        return self

    @property
    def name(self) -> Identifier:
        """The name of a block."""
        return getattr(self, "_name", None)

    @name.setter
    def name(self, value: Identifier):
        if value is None:
            setattr(self, "_name", None)
            return
        setattr(self, "_name", Identifier(value))

    @property
    def states(self) -> list:
        """The list of Vanilla block states and their values that the block can have, expressed in key/value pairs."""
        return getattr2(self, "_states", [])

    @states.setter
    def states(self, value: list):
        if value is None:
            self.states = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_states", value)

    @property
    def tags(self) -> Molang:
        """A condition using Molang queries that results to true/false that can be used to query for blocks with certain tags."""
        return getattr(self, "_tags", None)

    @tags.setter
    def tags(self, value: Molang):
        if value is None:
            setattr(self, "_tags", None)
            return
        setattr(self, "_tags", Molang(value))


class Filter:
    """Sets rules for under what conditions the block can be placed/survive"""

    def __init__(
        self,
        allowed_faces: list[BlockFace] = None,
        block_filter: list[BlockDescriptor] = None,
    ):
        self.allowed_faces = allowed_faces
        self.block_filter = block_filter

    @property
    def __dict__(self) -> dict:
        data = {
            "allowed_faces": [x._value_ for x in self.allowed_faces],
            "block_filter": [],
        }
        for v in self.block_filter:
            data["block_filter"].append(v.__dict__)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.allowed_faces = [BlockFace[x] for x in data.pop("allowed_faces")]
        for f in data.pop("block_filter"):
            self.block_filter.append(BlockDescriptor.from_dict(f))
        return self

    @property
    def allowed_faces(self) -> list[BlockFace]:
        """List of any of the following strings describing which face(s) this block can be placed on: "up", "down", "north", "south", "east", "west", "side", "all". Limited to 6 faces."""
        return getattr(self, "_allowed_faces", [])

    @allowed_faces.setter
    def allowed_faces(self, value: list[BlockFace]):
        if value is None:
            setattr(self, "_allowed_faces", [])
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list[BlockFace] but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_allowed_faces", value)

    @property
    def block_filter(self) -> list[BlockDescriptor]:
        """List of blocks that this block can be placed against in the "allowed_faces" direction. Limited to 64 blocks. Each block in this list can either be specified as a String (block name) or as a BlockDescriptor. A BlockDescriptor is an object that allows you to reference a block (or multiple blocks) based on its tags, or based on its name and states."""
        return getattr(self, "_block_filter", [])

    @block_filter.setter
    def block_filter(self, value: list[BlockDescriptor]):
        if value is None:
            setattr(self, "_block_filter", [])
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list[BlockDescriptor] but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_block_filter", value)

    # FACE

    def get_face(self, index: int) -> BlockFace:
        return self.allowed_faces[index]

    def add_face(self, face: BlockFace):
        if not isinstance(face, BlockFace):
            raise TypeError(
                f"Expected BlockFace but got '{face.__class__.__name__}' instead"
            )
        self.allowed_faces.append(face)
        return face

    def remove_face(self, index: int) -> BlockFace:
        return self.allowed_faces.pop(index)

    def clear_faces(self) -> Self:
        self.allowed_faces = []
        return self

    # FILTER

    def get_filter(self, index: int) -> BlockFace:
        return self.block_filter[index]

    def add_filter(self, filter: BlockDescriptor) -> BlockDescriptor:
        if not isinstance(filter, BlockDescriptor):
            raise TypeError(
                f"Expected BlockDescriptor but got '{filter.__class__.__name__}' instead"
            )
        self.block_filter.append(filter)
        return filter

    def remove_filter(self, index: int) -> BlockDescriptor:
        return self.block_filter.pop(index)

    def clear_filters(self) -> Self:
        self.block_filter = []
        return self


@block_component_type
class PlacementFilterComponent(BlockComponent):
    """Sets rules for under what conditions the block can be placed/survive"""

    id = Identifier("placement_filter")

    def __init__(self, conditions: list[Filter] = None):
        self.conditions = conditions

    def __iter__(self):
        for i in self.conditions:
            yield i

    @property
    def __dict__(self) -> dict:
        data = {"conditions": []}
        for v in self.conditions:
            data["conditions"].append(v.__dict__)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        for c in data.pop("conditions"):
            self.conditions.append(Filter.from_dict(c))
        return self

    @property
    def conditions(self) -> list[Filter]:
        """List of conditions where the block can be placed/survive. Limited to 64 conditions."""
        return getattr2(self, "_conditions", [])

    @conditions.setter
    def conditions(self, value: list[Filter]):
        if value is None:
            setattr(self, "_conditions", [])
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_conditions", value)

    # CONDITION

    def add_condition(self, filter: Filter) -> Filter:
        if not isinstance(filter, Filter):
            raise TypeError(
                f"Expected Filter but got '{filter.__class__.__name__}' instead"
            )
        self.conditions.append(filter)
        return filter

    def remove_condition(self, index: int) -> Filter:
        return self.conditions.pop(index)

    def clear_conditions(self) -> Self:
        self.conditions = []
        return self


@block_component_type
class QueuedTickingComponent(BlockComponent):
    """Triggers the specified event, either once, or at a regular interval equal to a number of ticks randomly chosen from the interval_range provided"""

    id = Identifier("queued_ticking")

    def __init__(
        self, interval_range: list[int], on_tick: Trigger, looping: bool = None
    ):
        self.interval_range = interval_range
        self.on_tick = on_tick
        self.looping = looping

    @property
    def __dict__(self) -> dict:
        data = {"interval_range": self.interval_range, "on_tick": self.on_tick.__dict__}
        if self.looping is not None:
            data["looping"] = self.looping
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.interval_range = data.pop("interval_range")
        self.on_tick = Trigger.from_dict(data.pop("on_tick"))
        return self

    @property
    def interval_range(self) -> list[int]:
        """A range of values, specified in ticks, that will be used to decide the interval between times this event triggers. Each interval will be chosen randomly from the range, so the times between this event triggering will differ given an interval_range of two different values. If the values in the interval_range are the same, the event will always be triggered after that number of ticks."""
        return getattr(self, "_interval_range")

    @interval_range.setter
    def interval_range(self, value: list[int]):
        if isinstance(value, int):
            self.interval_range = [value, value]
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_interval_range", value)

    @property
    def on_tick(self) -> Trigger:
        """The event that will be triggered once or on an interval."""
        return getattr(self, "_on_tick")

    @on_tick.setter
    def on_tick(self, value: Trigger):
        if not isinstance(value, Trigger):
            raise TypeError(
                f"Expected Trigger but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_on_tick", value)

    @property
    def looping(self) -> bool:
        """Does the event loop? If false, the event will only be triggered once, after a delay equal to a number of ticks randomly chosen from the interval_range. If true, the event will loop, and each interval between events will be equal to a number of ticks randomly chosen from the interval_range."""
        return getattr(self, "_looping", None)

    @looping.setter
    def looping(self, value: bool):
        if value is None:
            setattr(self, "_looping", None)
            return
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_looping", value)


@block_component_type
class RandomTickingComponent(BlockComponent):
    """Triggers the specified event randomly based on the random tick speed gamerule. The random tick speed determines how often blocks are updated. Some other examples of game mechanics that use random ticking are crop growth and fire spreading"""

    id = Identifier("random_ticking")

    def __init__(self, on_tick: Trigger):
        self.on_tick = on_tick

    @property
    def __dict__(self) -> dict:
        data = {"on_tick": self.on_tick.__dict__}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.on_tick = Trigger.from_dict(data.pop("on_tick"))
        return self

    @property
    def on_tick(self) -> Trigger:
        """The event that will be triggered on random ticks."""
        return getattr(self, "_on_tick")

    @on_tick.setter
    def on_tick(self, value: Trigger):
        if not isinstance(value, Trigger):
            raise TypeError(
                f"Expected Trigger but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_on_tick", value)


@block_component_type
class TransformationComponent(BlockComponent):
    """The block's translation, rotation and scale with respect to the center of its world position"""

    id = Identifier("transformation")

    def __init__(
        self,
        rotation: list[float] = None,
        translation: list[float] = None,
        scale: list[float] = None,
    ):
        self.rotation = rotation
        self.translation = translation
        self.scale = scale

    @classmethod
    def rotate(cls, x: int, y: int, z: int) -> Self:
        self = cls.__new__(cls)
        self.rotation = [x, y, z]
        return self

    @classmethod
    def offset(cls, x: int, y: int, z: int) -> Self:
        self = cls.__new__(cls)
        self.translation = [x, y, z]
        return self

    @classmethod
    def scaled(cls, x: int, y: int, z: int) -> Self:
        self = cls.__new__(cls)
        self.scale = [x, y, z]
        return self

    @property
    def __dict__(self) -> dict:
        data = {}
        if self.rotation is not None:
            data["rotation"] = self.rotation
        if self.translation is not None:
            data["translation"] = self.translation
        if self.scale is not None:
            data["scale"] = self.scale
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "rotation" in data:
            self.rotation = data.pop("rotation")
        if "translation" in data:
            self.translation = data.pop("translation")
        if "scale" in data:
            self.scale = data.pop("scale")
        return self

    @property
    def rotation(self) -> list[float]:
        return getattr(self, "_rotation", None)

    @rotation.setter
    def rotation(self, value: list[float]):
        if value is None:
            setattr(self, "_rotation", None)
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_rotation", value)

    @property
    def translation(self) -> list[float]:
        return getattr(self, "_translation", None)

    @translation.setter
    def translation(self, value: list[float]):
        if value is None:
            setattr(self, "_translation", None)
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_translation", value)

    @property
    def scale(self) -> list[float]:
        return getattr(self, "_scale", None)

    @scale.setter
    def scale(self, value: list[float]):
        if value is None:
            setattr(self, "_scale", None)
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_scale", value)


@block_component_type
class UnitCubeComponent(BlockComponent):
    """Specifies that a unit cube is to be used with tessellation."""

    id = Identifier("unit_cube")

    def __init__(self): ...

    @property
    def __dict__(self) -> dict:
        return {}

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        return self


@block_component_type
class BlockTagsComponent(BlockComponent):
    id = Identifier("tags")

    def __init__(self, tags: list[Identifier] = None):
        self.tags = tags

    @property
    def __dict__(self) -> dict:
        return [str(x) for x in self.tags]

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        for tag in data:
            self.tags.append(Identifier(tag))
        return self

    @property
    def tags(self) -> list[Identifier]:
        return getattr2(self, "_tags", [])

    @tags.setter
    def tags(self, value: list[Identifier]):
        if value is None:
            self.tags = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_tags", value)

    def get_tag(self, index: int) -> Identifier | None:
        return self.tags[index]

    def add_tag(self, tag: Identifier) -> Self:
        self.tags.append(Identifier(tag))
        return self

    def remove_tag(self, index: int) -> Identifier:
        return self.tags.pop(index)

    def clear_tags(self) -> Self:
        self.tags = []
        return self


# TRAITS


class BlockTrait:
    def __init__(self, enabled_states: list[BlockState]):
        self.enabled_states = enabled_states

    def __str__(self) -> str:
        return "BlockTrait{" + str(self.id) + "}"

    def __iter__(self):
        for es in zip(*self.enabled_states):
            for s in es:
                yield s

    def __getitem__(self, index: int):
        return self.enabled_states[index]

    @property
    def __dict__(self) -> dict:
        data = {"enabled_states": [str(x.id) for x in self.enabled_states]}
        return data

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier(value))

    @property
    def enabled_states(self) -> list[BlockState]:
        """Which states to enable. Must specify at least one."""
        return getattr(self, "_enabled_states", [])

    @enabled_states.setter
    def enabled_states(self, value: list[BlockState]):
        if value is None:
            self.enabled_states = []
        elif isinstance(value, list):
            v = []
            for x in value:
                if not issubclass(x, BlockState):
                    raise TypeError(
                        f"Expected BlockState but got '{x.__class__.__name__}' instead"
                    )
                v.append(x())
            setattr(self, "_enabled_states", v)
        else:
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "enabled_states" in data:
            self.enabled_states = data.pop("enabled_states")
        return self


INSTANCE.create_registry(Registries.BLOCK_TRAIT, BlockTrait)


def block_trait(cls):
    """
    Add this block trait to the registry
    """

    def wrapper():
        if not issubclass(cls, BlockTrait):
            raise TypeError(f"Expected BlockTrait but got '{cls.__name__}' instead")
        return INSTANCE.register(Registries.BLOCK_TRAIT, cls.id, cls)

    return wrapper()


@block_trait
class PlacementDirectionTrait(BlockTrait):
    """Adds the CardinalDirectionState and/or FacingDirectionState states and setter function to the block. The values of these states are set when the block is placed."""

    id = Identifier("placement_direction")

    def __init__(
        self, enabled_states: list[BlockState] = [], y_rotation_offset: float = 0.0
    ):
        for state in enabled_states:
            if not issubclass(state, (CardinalDirectionState, FacingDirectionState)):
                raise TypeError(
                    f"Expected CardinalDirectionState or FacingDirectionState but got '{state.__class__.__name__}' instead"
                )
        BlockTrait.__init__(self, enabled_states)
        if y_rotation_offset not in [0.0, 90.0, 180.0, 270.0, 0, 90, 180, 270]:
            raise ValueError(y_rotation_offset)
        self.y_rotation_offset = y_rotation_offset

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        if self.y_rotation_offset != 0:
            data["y_rotation_offset"] = self.y_rotation_offset
        return data

    @property
    def y_rotation_offset(self) -> float:
        """The y rotation offset to apply to the block. Must be [0.0, 90.0, 180.0, 270.0]. Default is 0, meaning if the player is facing north, the "minecraft:cardinal_direction" and/or minecraft:facing_direction state will be north."""
        return getattr(self, "_y_rotation_offset", 0.0)

    @y_rotation_offset.setter
    def y_rotation_offset(self, value: float):
        if value is None:
            self.y_rotation_offset = 0.0
        elif isinstance(value, float):
            setattr(self, "_y_rotation_offset", value)
        else:
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        if "y_rotation_offset" in data:
            self.y_rotation_offset = data.pop("y_rotation_offset")
        return self

    @classmethod
    def cardinal(cls) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([CardinalDirectionState])`
        states: ["north", "south", "east", "west"]
        """
        self = cls.__new__(cls)
        enabled_states = [CardinalDirectionState]
        BlockTrait.__init__(self, enabled_states)
        self.y_rotation_offset = 0.0
        return self

    @classmethod
    def facing(cls) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([FacingDirectionState])`
        states: ["down", "up", "north", "south", "east", "west"]
        """
        self = cls.__new__(cls)
        enabled_states = [FacingDirectionState]
        BlockTrait.__init__(self, enabled_states)
        self.y_rotation_offset = 0.0
        return self

    @classmethod
    def all(cls) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([CardinalDirectionState, FacingDirectionState])`
        """
        self = cls.__new__(cls)
        enabled_states = [CardinalDirectionState, FacingDirectionState]
        BlockTrait.__init__(self, enabled_states)
        self.y_rotation_offset = 0.0
        return self


@block_trait
class PlacementPositionTrait(BlockTrait):
    """Adds the BlockFaceState and/or VerticalHalfState BlockStates. The value of these state(s) are set when the block is placed."""

    id = Identifier("placement_position")

    def __init__(self, enabled_states: list[BlockState] = []):
        for state in enabled_states:
            if not issubclass(state, (BlockFaceState, VerticalHalfState)):
                raise TypeError(
                    f"Expected BlockFaceState or VerticalHalfState but got '{state.__class__.__name__}' instead"
                )
        BlockTrait.__init__(self, enabled_states)

    @classmethod
    def block_face(cls) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([BlockFaceState])`
        State: ["down", "up", "north", "south", "east", "west"]
        """
        self = cls.__new__(cls)
        enabled_states = [BlockFaceState]
        BlockTrait.__init__(self, enabled_states)
        return self

    @classmethod
    def vertical_half(cls) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([VerticalHalfState])`
        State: ["bottom", "up"]
        """
        self = cls.__new__(cls)
        enabled_states = [VerticalHalfState]
        BlockTrait.__init__(self, enabled_states)
        return self

    @classmethod
    def all(cls) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([BlockFaceState, VerticalHalfState])`
        """
        self = cls.__new__(cls)
        enabled_states = [BlockFaceState, VerticalHalfState]
        BlockTrait.__init__(self, enabled_states)
        return self


# BLOCK


class BlockPermutation:
    def __init__(
        self,
        condition: Molang | str,
        components: dict[Identifier, BlockComponent] = None,
    ):
        self.condition = Molang(condition)
        self.components: dict[Identifier, BlockComponent] = components

    def __str__(self) -> str:
        return stringify(self, ["condition"])

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.condition = Molang(data.pop("condition"))
        for k, v in data.pop("components").items():
            id = Identifier(k)
            clazz = INSTANCE.get_registry(Registries.BLOCK_COMPONENT_TYPE).get(id)
            if clazz is None:
                raise ComponentNotFoundError(repr(id))
            self.components[id] = clazz.from_dict(v)
        return self

    @property
    def __dict__(self) -> dict:
        data = {"condition": str(self.condition), "components": {}}
        for k, v in self.components.items():
            data["components"][str(k)] = v.__dict__
        return data

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

    @property
    def components(self) -> dict[Identifier, BlockComponent]:
        return getattr2(self, "_components", {})

    @components.setter
    def components(self, value: dict[Identifier, BlockComponent]):
        if value is None:
            self.components = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_components", value)

    def add_component(self, component: BlockComponent) -> BlockComponent:
        if not isinstance(component, BlockComponent):
            raise TypeError(
                f"Expected BlockComponent but got '{component.__class__.__name__}' instead"
            )
        self.components[component.id] = component
        return component

    def get_component(self, id: Identifier | str) -> BlockComponent:
        i = Identifier.parse(id)
        return self.components[i]

    def remove_component(self, id: Identifier | str) -> BlockComponent:
        i = Identifier.parse(id)
        e = self.components[i]
        del self.components[i]
        return e

    def clear_components(self) -> Self:
        self.components = {}
        return self


@dataclass
class BlockSettings:
    """
    Configure common settings for blocks
    """

    collidable: bool = True
    sound_group: str = None
    resistance: float = None
    hardness: float = None
    slipperiness: float = None
    loot_table: Identifier = None
    burnable: bool = False
    luminance: int = None
    map_color: str = None

    def color(self, color: str) -> Self:
        self.map_color = color
        return self

    def no_collision(self) -> Self:
        self.collidable = False
        return self

    def set_slipperiness(self, slipperiness: float) -> Self:
        self.slipperiness = slipperiness
        return self

    def sounds(self, sound_group: str) -> Self:
        self.sound_group = sound_group
        return self

    def set_luminance(self, luminance: int) -> Self:
        self.luminance = luminance
        return self

    def strength(self, hardness: float, resistance: float = None) -> Self:
        self.hardness = hardness
        self.resistance = hardness if resistance is None else resistance
        return self

    def breakInstantly(self) -> Self:
        self.strength(0.0, 0.0)
        return self

    def dropsNothing(self) -> Self:
        self.loot_table = "loot_tables/empty.json"
        return self

    def dropsLike(self, source) -> Self:
        self.loot_table = source.identifier
        return self

    def is_burnable(self) -> Self:
        self.burnable = True
        return self

    def set_hardness(self, hardness: float) -> Self:
        self.hardness = hardness
        return self

    def set_resistance(self, resistance: float) -> Self:
        self.resistance = resistance
        return self


class Block(JsonFile, Identifiable):
    """
    Represents a Block.
    """

    id = Identifier("block")
    EXTENSION = ".json"
    FILENAME = "block"
    DIRNAME = "blocks"

    def __init__(
        self,
        identifier: Identifier | str,
        menu_category: MenuCategory = None,
        components: dict[str, BlockComponent] = None,
        permutations: list[BlockPermutation] = None,
        events: dict[Identifier, Event] = None,
        traits: dict[Identifier, BlockTrait] = None,
        states: dict[Identifier, list[str]] = None,
        sound_group: str = None,
    ):
        Identifiable.__init__(self, identifier)
        self.identifier = identifier
        self.menu_category = menu_category
        self.components = components
        self.permutations = permutations
        self.events = events
        self.traits = traits
        self.states = states
        self.sound_group = sound_group

        col = self.get_collision_shape()
        if col is not None:
            self.add_component(CollisionBoxComponent(*col))
        sel = self.get_selection_shape()
        if sel is not None:
            self.add_component(SelectionBoxComponent(*sel))

    def __str__(self) -> str:
        return "Block{" + str(self.identifier) + "}"

    @property
    def __dict__(self) -> dict:
        block = {"description": {"identifier": str(self.identifier)}}
        if self.menu_category:
            block["description"]["menu_category"] = self.menu_category.__dict__

        if self.traits:
            block["description"]["traits"] = {}
            for k, v in self.traits.items():
                block["description"]["traits"][str(k)] = v.__dict__

        if self.states:
            block["description"]["states"] = {}
            for k, v in self.states.items():
                block["description"]["states"].update(v.__dict__)

        if self.components:
            block["components"] = {}
            for k, v in self.components.items():
                block["components"][str(k)] = v.__dict__

        if self.permutations:
            block["permutations"] = []
            for v in self.permutations:
                block["permutations"].append(v.__dict__)

        if self.events:
            block["events"] = {}
            for key, events in self.events.items():
                d = {}
                for k, v in events.items():
                    d[k.path] = v.__dict__
                block["events"][str(key)] = d

        data = {"format_version": VERSION["BLOCK"], str(self.id): block}
        if self.type:
            data["type"] = str(self.type)
        return data

    @property
    def type(self) -> Identifier:
        return getattr(self, "_type", None)

    @type.setter
    def type(self, value: Identifier):
        setattr(self, "_type", Identifier(value))

    @property
    def menu_category(self) -> MenuCategory:
        return getattr(self, "_menu_category", None)

    @menu_category.setter
    def menu_category(self, value: MenuCategory):
        if value is None:
            setattr(self, "_menu_category", None)
            return None
        if not isinstance(value, MenuCategory):
            raise TypeError(
                f"Expected MenuCategory but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_menu_category", value)

    @property
    def components(self) -> dict[str, BlockComponent]:
        return getattr2(self, "_components", {})

    @components.setter
    def components(self, value: dict[str, BlockComponent]):
        if value is None:
            self.components = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_components", value)

    @property
    def permutations(self) -> list[BlockPermutation]:
        return getattr2(self, "_permutations", [])

    @permutations.setter
    def permutations(self, value: list[BlockPermutation]):
        if value is None:
            self.permutation = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_permutations", value)

    @property
    def events(self) -> dict[Identifier, Event]:
        return getattr2(self, "_events", {})

    @events.setter
    def events(self, value: dict[Identifier, Event]):
        if value is None:
            self.events = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_events", value)

    @property
    def states(self) -> dict[Identifier, BlockState]:
        return getattr2(self, "_states", {})

    @states.setter
    def states(self, value: dict[Identifier, BlockState]):
        if value is None:
            self.states = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_states", value)

    @property
    def traits(self) -> dict[Identifier, BlockTrait]:
        return getattr2(self, "_traits", {})

    @traits.setter
    def traits(self, value: dict[Identifier, BlockTrait]):
        if value is None:
            self.traits = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_traits", value)

    @property
    def sound_group(self) -> str | None:
        return getattr(self, "_sound_group", None)

    @sound_group.setter
    def sound_group(self, value: str | None):
        if value is None:
            setattr(self, "_sound_group", None)
            return
        setattr(self, "_sound_group", str(value))

    # Read-Only

    @property
    def hardness(self) -> float:
        v = self.get_component("destructible_by_mining")
        return 0.0 if v is None else v

    @property
    def resistance(self) -> float:
        v = self.get_component("destructible_by_explosion")
        return 0.0 if v is None else v

    @property
    def map_color(self) -> str:
        return self.get_component("map_color")

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = BlockLoader()
        loader.validate(data)
        return loader.load(data)

    @classmethod
    def from_settings(cls, identifier: Identifier, settings: BlockSettings) -> Self:
        """
        Create a block using block settings

        :param identifier: The ID of the block
        :type identifier: Identifier
        :param settings: The block settings
        :type settings: BlockSettings
        :rtype: Block
        """
        if not isinstance(settings, BlockSettings):
            raise TypeError(
                f"Expected BlockSettings but got '{settings.__class__.__name__}' instead"
            )
        self = cls.__new__(cls)
        self.identifier = identifier

        if settings.collidable is not None:
            self.add_component(CollisionBoxComponent(settings.collidable))

        if settings.sound_group is not None:
            self.sound_group = settings.sound_group

        if settings.resistance is not None:
            self.add_component(DestructibleByExplosionComponent(settings.resistance))

        if settings.hardness is not None:
            self.add_component(DestructibleByMiningComponent(settings.hardness))

        if settings.slipperiness is not None:
            self.add_component(FrictionComponent(settings.slipperiness))

        if settings.loot_table is not None:
            self.add_component(LootComponent(settings.loot_table))

        # use molang?
        if settings.luminance is not None:
            self.add_component(LightEmissionComponent(settings.luminance))

        if settings.map_color is not None:
            self.add_component(MapColorComponent(settings.map_color))

        if settings.burnable:
            self.add_component(FlammableComponent(0, 0))

        return self

    def translation_key(self) -> str:
        return f"tile.{str(self.id)}.name"

    def stack(self):
        return ItemStack(self.identifier)

    def get_collision_shape(self) -> tuple[list, list]:
        """
        Override this method to add a custom collision shape

        :return: The SIZE and ORIGIN
        :rtype: tuple[list, list]
        """
        return None

    def get_selection_shape(self) -> tuple[list, list]:
        """
        Override this method to add a custom selection shape

        :return: The SIZE and ORIGIN
        :rtype: tuple[list, list]
        """
        return None

    # COMPONENT

    def add_component(self, component: BlockComponent) -> BlockComponent:
        if not isinstance(component, BlockComponent):
            raise TypeError(
                f"Expected BlockComponent but got '{component.__class__.__name__}' instead"
            )
        if isinstance(component, Trigger):
            component.event.namespace = self.identifier.namespace
        self.components[component.id] = component
        return component

    def get_component(self, id: Identifier) -> BlockComponent:
        x = id.id if isinstance(id, BlockComponent) else Identifier(id)
        return self.components.get(x)

    def remove_component(self, id: str) -> BlockComponent:
        x = id.id if isinstance(id, BlockComponent) else Identifier(id)
        return self.components.pop(x)

    def clear_components(self) -> Self:
        """
        Removes all components
        """
        self.components.clear()
        return self

    # EVENT
    def _event_id(self, id: Identifier | str):
        if id is None:
            return "default"
        elif isinstance(id, Identifier):
            return id
        else:
            return self.identifier.copy_with_path(id)

    def add_event(self, id: Identifier | str, event: Event) -> Event:
        if isinstance(event, Event):
            k = self._event_id(id)
            if k in self.events:
                self.events[k][event.id] = event
                return event
            self.events[k] = {}
            return self.add_event(id, event)
        elif isinstance(event, list):
            x = Sequence()
            for e in event:
                x.add_event(e)
            return self.add_event(id, x)
        else:
            raise TypeError(
                f"Expected BlockEvent but got '{event.__class__.__name__}' instead"
            )

    def get_event(self, id: Identifier | str) -> Event:
        k = self._event_id(id)
        return self.events.get(k)

    def remove_event(self, id: Identifier | str) -> Event:
        i = Identifier.parse(id)
        return self.events.pop(i)

    def clear_events(self) -> Self:
        """
        Removes all events
        """
        self.events.clear()
        return self

    # PERMUTATION

    def add_permutation(self, permutation: BlockPermutation) -> BlockPermutation:
        if not isinstance(permutation, BlockPermutation):
            raise TypeError(
                f"Expected BlockPermutation but got '{permutation.__class__.__name__}' instead"
            )
        self.permutations.append(permutation)
        return permutation

    def get_permutation(self, index: int) -> BlockPermutation:
        return self.permutations[index]

    def remove_permutation(self, index: int) -> BlockPermutation:
        p = self.get_permutation(index)
        del self.permutations[index]
        return p

    def clear_permutation(self) -> Self:
        """
        Removes all permutations
        """
        self.permutations.clear()
        return self

    # TRAIT

    def add_trait(self, trait: BlockTrait) -> BlockTrait:
        if not isinstance(trait, BlockTrait):
            raise TypeError(
                f"Expected BlockTrait but got '{trait.__class__.__name__}' instead"
            )
        self.traits[trait.id] = trait
        return trait

    def get_trait(self, id: str) -> BlockTrait:
        x = id.id if isinstance(id, BlockTrait) else Identifier(id)
        return self.traits.get(x)

    def remove_trait(self, id: str) -> BlockTrait:
        x = id.id if isinstance(id, BlockTrait) else Identifier(id)
        return self.traits.pop(x)

    def clear_trait(self) -> Self:
        """
        Removes all traits
        """
        self.traits.clear()
        return self

    # STATE

    def add_state(self, state: BlockState) -> BlockState:
        if not isinstance(state, BlockState):
            raise TypeError(
                f"Expected BlockState but got '{state.__class__.__name__}' instead"
            )
        self.states[state.id] = state
        return state

    def get_state(self, id: Identifier | str) -> BlockState:
        x = id.id if isinstance(id, BlockState) else Identifier(id)
        return self.states.get(x)

    def remove_state(self, id: Identifier | str) -> BlockState:
        x = id.id if isinstance(id, BlockState) else Identifier(id)
        return self.states.pop(x)

    def clear_state(self) -> Self:
        """
        Removes all states
        """
        self.states.clear()
        return self


class BlockLoader(Loader):
    name = "Block"

    def __init__(self):
        from .schemas import BlockSchema1

        Loader.__init__(self, Block)
        self.add_schema(BlockSchema1, "1.20.51")


# TYPES

INSTANCE.create_registry(Registries.BLOCK_TYPE, Block)


def block_type(cls):
    """
    Add this block type to the registry
    """

    def wrapper():
        return INSTANCE.register(Registries.BLOCK_TYPE, cls.type, cls)

    return wrapper()
