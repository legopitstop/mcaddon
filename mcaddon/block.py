from typing import Self
from molang import Molang
from dataclasses import dataclass

from . import VERSION
from .pack import behavior_pack, resource_pack, ResourcePack
from .exception import ComponentNotFoundError
from .registry import INSTANCE, Registries
from .constant import RenderMethod, BlockFace, MapColor
from .file import JsonFile, Loader
from .math import Vector3, Range
from .util import (
    getattr2,
    setattr2,
    stringify,
    clearitems,
    removeitem,
    getitem,
    additem,
    Misc,
    Box,
    Identifier,
    MenuCategory,
    Identifiable,
)
from .state import (
    BlockProperty,
    CardinalDirectionState,
    FacingDirectionState,
    BlockFaceState,
    VerticalHalfState,
)
from .event import *


class BlockComponent(Misc):
    def __repr__(self):
        return "BlockComponent{" + str(self.id) + "}"

    def __str__(self) -> str:
        return str(self.id)

    def __call__(self, ctx) -> int:
        return self.execute(ctx)

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier.of(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        raise NotImplementedError()

    def execute(self, ctx) -> int:
        return 0

    def generate(self, ctx) -> None:
        """
        Called when this component is added to the Block

        :type ctx: Block
        """
        ...


class SimpleBlockComponent(BlockComponent):
    def __init__(self, value):
        self.value = value

    def jsonify(self):
        data = self.value
        return data

    @staticmethod
    def from_dict(data) -> Self:
        return SimpleBlockComponent(data)

    @property
    def clazz(self):
        return getattr(self, "_clazz", None)

    @clazz.setter
    def clazz(self, value):
        setattr(self, "_clazz", value)

    @property
    def value(self):
        return getattr(self, "_value")

    @value.setter
    def value(self, value):
        if self.clazz is not None and not isinstance(value, self.clazz):
            raise TypeError(
                f"Expected {self.clazz.__name__} but got '{value.__class__.__name__}' instead"
            )
        self.on_update("value", value)
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
    """Describes event for this block. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blocktriggers/minecraftblock_on_fall_on?view=minecraft-bedrock-stable)"""

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

    def jsonify(self):
        data = super().jsonify()
        if self.min_fall_distance is not None:
            data["min_fall_distance"] = self.min_fall_distance
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        min_fall_distance = (
            data.pop("min_fall_distance") if "min_fall_distance" in data else 0
        )
        tr = Trigger(**data)
        return OnFallOnComponent(tr.event, min_fall_distance, tr.condition, tr.target)

    @property
    def min_fall_distance(self) -> float:
        """The event executed on the block, defaults to 'on_fall_on'"""
        return getattr(self, "_min_fall_distance", None)

    @min_fall_distance.setter
    def min_fall_distance(self, value: float):
        if value is None:
            return
        self.on_update("min_fall_distance", float(value))
        setattr(self, "_min_fall_distance", float(value))


@block_component_type
class OnInteractComponent(Trigger, BlockComponent):
    """Describes event for this block. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blocktriggers/minecraftblock_on_interact?view=minecraft-bedrock-stable)"""

    id = Identifier("on_interact")

    def __init__(
        self, event: str = "on_interact", condition: str = None, target: str = None
    ):
        Trigger.__init__(self, event, condition, target)


@block_component_type
class OnPlacedComponent(Trigger, BlockComponent):
    """Describes event for this block. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blocktriggers/minecraftblock_on_placed?view=minecraft-bedrock-stable)"""

    id = Identifier("on_placed")

    def __init__(
        self, event: str = "on_placed", condition: str = None, target: str = None
    ):
        Trigger.__init__(self, event, condition, target)


@block_component_type
class OnPlayerDestroyedComponent(Trigger, BlockComponent):
    """Describes event for this block. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blocktriggers/minecraftblock_on_player_destroyed?view=minecraft-bedrock-stable)"""

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
    """Describes event for this block. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blocktriggers/minecraftblock_on_player_placing?view=minecraft-bedrock-stable)"""

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
    """Describes event for this block. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blocktriggers/minecraftblock_on_step_off?view=minecraft-bedrock-stable)"""

    id = Identifier("on_step_off")

    def __init__(
        self, event: str = "on_step_off", condition: str = None, target: str = None
    ):
        Trigger.__init__(self, event, condition, target)


@block_component_type
class OnStepOnComponent(Trigger, BlockComponent):
    """Describes event for this block. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blocktriggers/minecraftblock_on_step_on?view=minecraft-bedrock-stable)"""

    id = Identifier("on_step_on")

    def __init__(
        self, event: str = "on_step_on", condition: str = None, target: str = None
    ):
        Trigger.__init__(self, event, condition, target)


@block_component_type
class BoneVisabilityComponent(BlockComponent):
    """Tells whether the bone should be visible or not (value)."""

    id = Identifier("bone_visibility")

    def __init__(self, bones: dict[str, Molang | bool] = None):
        self.bones = bones

    def jsonify(self) -> dict:
        data = {"bones": {}}
        for k, v in self.bones.items():
            data["bones"][k] = str(v)
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return BoneVisabilityComponent(**data)

    @property
    def bones(self) -> dict[str, Molang | bool]:
        return getattr2(self, "_bones", {})

    @bones.setter
    def bones(self, value: dict[str, Molang | bool]):
        self.on_update("bones", value)
        setattr2(self, "_bones", value, dict)

    def get_bone(self, bone: str) -> Molang | None:
        return getitem(self, "bones", bone)

    def add_bone(self, bone: str, condition: Molang) -> Molang:
        return additem(self, "bones", Molang(condition), bone, Molang)

    def remove_bone(self, bone: str) -> Molang:
        return removeitem(self, "bones", bone)

    def clear_bones(self) -> Self:
        """Remove all bones"""
        return clearitems(self, "bones")


@block_component_type
class BreathabilityComponent(SimpleBlockComponent):
    """"""

    id = Identifier("breathability")
    clazz = str


@block_component_type
class CollisionBoxComponent(BlockComponent, Box):
    """Defines the area of the block that collides with entities. If set to true, default values are used. If set to false, the block's collision with entities is disabled. If this component is omitted, default values are used. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_collision_box?view=minecraft-bedrock-stable)"""

    id = Identifier("collision_box")

    def __init__(
        self,
        origin: Vector3 | bool = Vector3(-8, 0 - 8),
        size: Vector3 = Vector3(16, 16, 16),
    ):
        if isinstance(origin, bool):
            if origin:
                origin = Vector3(-8, 0, -8)
                size = Vector3(16, 16, 16)
            else:
                origin = Vector3(0, 0, 0)
                size = Vector3(0, 0, 0)
        Box.__init__(self, origin, size)

    def jsonify(self) -> dict:
        data = super().as_dict()
        if self.is_cube():
            return True
        elif self.is_none():
            return False
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        if isinstance(data, bool):
            return (
                CollisionBoxComponent.cube() if data else CollisionBoxComponent.none()
            )
        origin = None
        if "origin" in data:
            origin = Vector3(*data.pop("origin"))
        size = None
        if "size" in data:
            size = Vector3(*data.pop("size"))
        return CollisionBoxComponent(origin, size)


@block_component_type
class SelectionBoxComponent(BlockComponent, Box):
    """Defines the area of the block that is selected by the player's cursor. If set to true, default values are used. If set to false, this block is not selectable by the player's cursor. If this component is omitted, default values are used. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_selection_box?view=minecraft-bedrock-stable)"""

    id = Identifier("selection_box")

    def __init__(
        self,
        origin: Vector3 | bool = Vector3(-8, 0, -8),
        size: Vector3 = Vector3(16, 16, 16),
    ):
        if isinstance(origin, bool):
            if origin:
                origin = Vector3(-8, 0, -8)
                size = Vector3(16, 16, 16)
            else:
                origin = Vector3(0, 0, 0)
                size = Vector3(0, 0, 0)
        Box.__init__(self, origin, size)

    def jsonify(self) -> dict:
        data = super().as_dict()
        if self.is_cube():
            return True
        elif self.is_none():
            return False
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        if isinstance(data, bool):
            return (
                SelectionBoxComponent.cube() if data else SelectionBoxComponent.none()
            )
        origin = None
        if "origin" in data:
            origin = Vector3(*data.pop("origin"))
        size = None
        if "size" in data:
            size = Vector3(*data.pop("size"))
        return SelectionBoxComponent(origin, size)


@block_component_type
class CraftingTableComponent(BlockComponent):
    """Makes your block into a custom crafting table which enables the crafting table UI and the ability to craft recipes. This component supports only "recipe_shaped" and "recipe_shapeless" typed recipes and not others like "recipe_furnace" or "recipe_brewing_mix". If there are two recipes for one item, the recipe book will pick the first that was parsed. If two input recipes are the same, crafting may assert and the resulting item may vary. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_crafting_table?view=minecraft-bedrock-stable)"""

    id = Identifier("crafting_table")

    def __init__(self, table_name: str, crafting_tags: list[str] = None):
        self.table_name = table_name
        self.crafting_tags = crafting_tags

    def jsonify(self) -> dict:
        data = {"crafting_tags": self.crafting_tags, "table_name": self.table_name}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        table_name = data.pop("table_name")
        crafting_tags = data.pop("crafting_tags")
        return CraftingTableComponent(table_name, crafting_tags)

    @property
    def crafting_tags(self) -> list[str]:
        """Defines the tags recipes should define to be crafted on this table. Limited to 64 tags. Each tag is limited to 64 characters."""
        return getattr2(self, "_crafting_tags", ["crafting_table"])

    @crafting_tags.setter
    def crafting_tags(self, value: list[str]):
        self.on_update("crafting_tags", value)
        setattr2(self, "_crafting_tags", value, list)

    @property
    def table_name(self) -> str:
        """Specifies the language file key that maps to what text will be displayed in the UI of this table. If the string given can not be resolved as a loc string, the raw string given will be displayed. If this field is omitted, the name displayed will default to the name specified in the "display_name" component. If this block has no "display_name" component, the name displayed will default to the name of the block."""
        return getattr(self, "_table_name")

    @table_name.setter
    def table_name(self, value: str):
        self.on_update("table_name", str(value))
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
    """Describes the destructible by explosion properties for this block. If set to true, the block will have the default explosion resistance. If set to false, this block is indestructible by explosion. If the component is omitted, the block will have the default explosion resistance [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_destructible_by_explosion?view=minecraft-bedrock-stable)"""

    id = Identifier("destructible_by_explosion")

    def __init__(self, explosion_resistance: float = None):
        self.explosion_resistance = explosion_resistance

    def jsonify(self) -> dict:
        data = {"explosion_resistance": self.explosion_resistance}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return DestructibleByExplosionComponent(**data)

    @property
    def explosion_resistance(self) -> float:
        """Sets the explosion resistance for the block. Greater values result in greater resistance to explosions. The scale will be different for different explosion power levels. A negative value or 0 means it will easily explode; larger numbers increase level of resistance."""
        return getattr(self, "_explosion_resistance")

    @explosion_resistance.setter
    def explosion_resistance(self, value: float):
        if value is None:
            return
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        self.on_update("explosion_resistance", value)
        setattr(self, "_explosion_resistance", value)


@block_component_type
class DestructibleByMiningComponent(BlockComponent):
    """Describes the destructible by mining properties for this block. If set to true, the block will take the default number of seconds to destroy. If set to false, this block is indestructible by mining. If the component is omitted, the block will take the default number of seconds to destroy. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_destructible_by_mining?view=minecraft-bedrock-stable)"""

    id = Identifier("destructible_by_mining")

    def __init__(self, seconds_to_destroy: float = None):
        self.seconds_to_destroy = seconds_to_destroy

    def jsonify(self) -> dict:
        data = {"seconds_to_destroy": self.seconds_to_destroy}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return DestructibleByMiningComponent(**data)

    @property
    def seconds_to_destroy(self) -> float:
        """Sets the number of seconds it takes to destroy the block with base equipment. Greater numbers result in greater mining times."""
        return getattr(self, "_seconds_to_destroy", None)

    @seconds_to_destroy.setter
    def seconds_to_destroy(self, value: float):
        if value is None:
            return
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float or int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("seconds_to_destroy", value)
        setattr(self, "_seconds_to_destroy", value)


@block_component_type
class BlockDisplayNameComponent(SimpleBlockComponent):
    """Specifies the language file key that maps to what text will be displayed when you hover over the block in your inventory and hotbar. If the string given can not be resolved as a loc string, the raw string given will be displayed. If this component is omitted, the name of the block will be used as the display name. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_display_name?view=minecraft-bedrock-stable)"""

    id = Identifier("display_name")
    clazz = str


@block_component_type
class FlammableComponent(BlockComponent):
    """Describes the flammable properties for this block. If set to true, default values are used. If set to false, or if this component is omitted, the block will not be able to catch on fire naturally from neighbors, but it can still be directly ignited. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_flammable?view=minecraft-bedrock-stable)"""

    id = Identifier("flammable")

    def __init__(
        self, catch_chance_modifier: int = None, destroy_chance_modifier: int = None
    ):
        self.catch_chance_modifier = catch_chance_modifier
        self.destroy_chance_modifier = destroy_chance_modifier

    def jsonify(self) -> dict:
        data = {}
        if self.catch_chance_modifier is not None:
            data["catch_chance_modifier"] = self.catch_chance_modifier
        if self.destroy_chance_modifier is not None:
            data["destroy_chance_modifier"] = self.destroy_chance_modifier
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        catch_chance_modifier = None
        destroy_chance_modifier = None
        if "catch_chance_modifier" in data:
            catch_chance_modifier = data.pop("catch_chance_modifier")
        if "destroy_chance_modifier" in data:
            destroy_chance_modifier = data.pop("destroy_chance_modifier")
        return FlammableComponent(catch_chance_modifier, destroy_chance_modifier)

    @property
    def catch_chance_modifier(self) -> int:
        """A modifier affecting the chance that this block will catch flame when next to a fire. Values are greater than or equal to 0, with a higher number meaning more likely to catch on fire. For a "catch_chance_modifier" greater than 0, the fire will continue to burn until the block is destroyed (or it will burn forever if the "destroy_chance_modifier" is 0). If the "catch_chance_modifier" is 0, and the block is directly ignited, the fire will eventually burn out without destroying the block (or it will have a chance to be destroyed if "destroy_chance_modifier" is greater than 0). The default value of 5 is the same as that of Planks."""
        return getattr(self, "_catch_chance_modifier", None)

    @catch_chance_modifier.setter
    def catch_chance_modifier(self, value: int):
        if value is None:
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("catch_chance_modifier", value)
        setattr(self, "_catch_chance_modifier", value)

    @property
    def destroy_chance_modifier(self) -> int:
        """A modifier affecting the chance that this block will be destroyed by flames when on fire. Values are greater than or equal to 0, with a higher number meaning more likely to be destroyed by fire. For a "destroy_chance_modifier" of 0, the block will never be destroyed by fire, and the fire will burn forever if the "catch_chance_modifier" is greater than 0. The default value of 20 is the same as that of Planks."""
        return getattr(self, "_destroy_chance_modifier", None)

    @destroy_chance_modifier.setter
    def destroy_chance_modifier(self, value: int):
        if value is None:
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("destroy_chance_modifier", value)
        setattr(self, "_destroy_chance_modifier", value)


@block_component_type
class FrictionComponent(BlockComponent):
    """Describes the friction for this block in a range of (0.0-0.9). Friction affects an entity's movement speed when it travels on the block. Greater value results in more friction. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_friction?view=minecraft-bedrock-stable)"""

    id = Identifier("friction")
    clazz = float

    def __init__(self, value: float):
        self.value = value

    @staticmethod
    def from_dict(data: dict) -> Self:
        return FrictionComponent(data)

    def jsonify(self) -> int:
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
        self.on_update("value", value)
        setattr(self, "_value", value)


@block_component_type
class GeometryComponent(BlockComponent):
    """The description identifier of the geometry file to use to render this block. This identifier must match an existing geometry identifier in any of the currently loaded resource packs. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_geometry?view=minecraft-bedrock-stable)"""

    id = Identifier("geometry")

    def __init__(
        self,
        geometry: str,
        bone_visibility: dict[str, Molang | bool] = None,
        culling: Identifiable = None,
    ):
        self.geometry = geometry
        self.bone_visibility = bone_visibility
        self.culling = culling

    def jsonify(self) -> dict:
        data = {"identifier": self.geometry}
        if self.bone_visibility:
            data["bone_visibility"] = {}
            for k, v in self.bone_visibility.items():
                data["bone_visibility"][k] = str(v)
        if self.culling:
            data["culling"] = str(self.culling)
        if not self.bone_visibility and not self.culling:
            return str(self.geometry)
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        if isinstance(data, str):
            return GeometryComponent(data)
        elif isinstance(data, dict):
            geometry = data.pop("identifier")
            bone_visibility = (
                data.pop("bone_visibility") if "bone_visibility" in data else {}
            )
            culling = data.pop("culling") if "culling" in data else None
            return GeometryComponent(geometry, bone_visibility, culling)

    @property
    def geometry(self) -> str:
        return getattr(self, "_geometry")

    @geometry.setter
    def geometry(self, value: str):
        self.on_update("geometry", str(value))
        setattr(self, "_geometry", str(value))

    @property
    def bone_visibility(self) -> dict[str, Molang | bool]:
        return getattr(self, "_bone_visibility", {})

    @bone_visibility.setter
    def bone_visibility(self, value: dict[str, Molang | bool]):
        self.on_update("bone_visibility", value)
        setattr2(self, "_bone_visibility", value, dict)

    @property
    def culling(self) -> Identifier:
        return getattr(self, "_culling")

    @culling.setter
    def culling(self, value: Identifiable):
        setattr(self, "_culling", Identifiable.of(value))


@block_component_type
class LightDampeningComponent(SimpleBlockComponent):
    """The amount that light will be dampened when it passes through the block, in a range (0-15). Higher value means the light will be dampened more. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_light_dampening?view=minecraft-bedrock-stable)"""

    id = Identifier("light_dampening")
    clazz = int

    def jsonify(self) -> int:
        data = 15 if self.value is None else self.value
        return data


@block_component_type
class LightEmissionComponent(SimpleBlockComponent):
    """The amount of light this block will emit in a range (0-15). Higher value means more light will be emitted. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_light_emission?view=minecraft-bedrock-stable)"""

    id = Identifier("light_emission")
    clazz = int

    def jsonify(self) -> str:
        data = 0 if self.value is None else self.value
        return data


@block_component_type
class LootComponent(SimpleBlockComponent):
    """The path to the loot table, relative to the behavior pack. Path string is limited to 256 characters. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_loot?view=minecraft-bedrock-stable)"""

    id = Identifier("loot")
    clazz = str

    @classmethod
    def empty(cls) -> Self:
        return LootComponent("loot_tables/empty.json")


@block_component_type
class MapColorComponent(BlockComponent):
    """Sets the color of the block when rendered to a map. The color is represented as a hex value in the format "#RRGGBB". May also be expressed as an array of [R, G, B] from 0 to 255. If this component is omitted, the block will not show up on the map. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_map_color?view=minecraft-bedrock-stable)"""

    id = Identifier("map_color")

    def __init__(self, value: MapColor | int):
        self.value = value

    def jsonify(self) -> dict:
        return hex(self.value).replace("0x", "#")

    @staticmethod
    def from_dict(data: dict) -> Self:
        return MapColorComponent(data)

    @property
    def value(self) -> int:
        return getattr(self, "_value")

    @value.setter
    def value(self, value: int | MapColor):
        if isinstance(value, MapColor):
            value = value._value_
        if isinstance(value, str):
            value = int(value.replace("#", "0x"), 16)
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("value", value)
        setattr(self, "_value", value)


class Material(Misc):
    """A material instance definition to map to a material instance in a geometry file. The material instance "*" will be used for any materials that don't have a match."""

    def __init__(
        self,
        texture: Identifiable,
        render_method: RenderMethod = RenderMethod.OPAQUE,
        ambient_occlusion: bool = True,
        face_dimming: bool = True,
    ):
        self.texture = texture
        self.ambient_occlusion = ambient_occlusion
        self.face_dimming = face_dimming
        self.render_method = render_method

    def jsonify(self) -> dict:
        data = {"texture": str(self.texture)}
        if self.render_method not in [None, RenderMethod.OPAQUE]:
            data["render_method"] = self.render_method.jsonify()
        if self.ambient_occlusion not in [None, True]:
            data["ambient_occlusion"] = self.ambient_occlusion
        if self.face_dimming not in [None, True]:
            data["face_dimming"] = self.face_dimming
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return Material(**data)

    @property
    def texture(self) -> Identifier:
        """Texture name for the material."""
        return getattr(self, "_texture")

    @texture.setter
    def texture(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("texture", id)
        setattr(self, "_texture", id)

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
        self.on_update("ambient_occlusion", value)
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
        self.on_update("face_dimming", value)
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
            return
        if isinstance(value, RenderMethod):
            self.on_update("render_method", value)
            setattr(self, "_render_method", value)
        else:
            self.render_method = RenderMethod.from_dict(value)


@block_component_type
class MaterialInstancesComponent(BlockComponent):
    """The material instances for a block. Maps face or material_instance names in a geometry file to an actual material instance. You can assign a material instance object to any of these faces: "up", "down", "north", "south", "east", "west", or "*". You can also give an instance the name of your choosing such as "my_instance", and then assign it to a face by doing "north":"my_instance". [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_material_instances?view=minecraft-bedrock-stable)"""

    id = Identifier("material_instances")

    def __init__(self, materials: dict[str, Material] = None):
        self.materials = materials

    def jsonify(self) -> dict:
        data = {}
        for k, v in self.materials.items():
            data[k] = v.jsonify()
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        materials = {}
        for k, v in data.items():
            materials[k] = Material.from_dict(v)
        return MaterialInstancesComponent(materials)

    @property
    def materials(self) -> dict[str, Material]:
        return getattr2(self, "_materials", {})

    @materials.setter
    def materials(self, value: dict[str, Material]):
        self.on_update("materials", value)
        setattr2(self, "_materials", value, dict)

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


class BlockDescriptor(Misc):
    def __init__(self, name: Identifiable = None, states: dict = None, tags: str = "1"):
        self.name = name
        self.states = states
        self.tags = tags

    def jsonify(self) -> dict:
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

    @staticmethod
    def from_dict(data: dict) -> Self:
        return BlockDescriptor(**data)

    @property
    def name(self) -> Identifier:
        """The name of a block."""
        return getattr(self, "_name", None)

    @name.setter
    def name(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("name", id)
        setattr(self, "_name", id)

    @property
    def states(self) -> list:
        """The list of Vanilla block states and their values that the block can have, expressed in key/value pairs."""
        return getattr2(self, "_states", {})

    @states.setter
    def states(self, value: dict):
        self.on_update("states", value)
        setattr2(self, "_states", value, dict)

    @property
    def tags(self) -> Molang:
        """A condition using Molang queries that results to true/false that can be used to query for blocks with certain tags."""
        return getattr(self, "_tags", None)

    @tags.setter
    def tags(self, value: Molang):
        if value is None:
            setattr(self, "_tags", None)
            return
        v = Molang(value)
        self.on_update("tags", v)
        setattr(self, "_tags", v)


class BlockFilter(Misc):
    """Sets rules for under what conditions the block can be placed/survive"""

    def __init__(
        self,
        allowed_faces: list[BlockFace] = None,
        block_filter: list[BlockDescriptor] = None,
    ):
        self.allowed_faces = allowed_faces
        self.block_filter = block_filter

    def jsonify(self) -> dict:
        data = {
            "allowed_faces": [x.jsonify() for x in self.allowed_faces],
            "block_filter": [],
        }
        for v in self.block_filter:
            data["block_filter"].append(v.jsonify())
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        allowed_faces = [BlockFace.from_dict(x) for x in data.pop("allowed_faces")]
        block_filter = []
        for f in data.pop("block_filter"):
            block_filter.append(BlockDescriptor.from_dict(f))
        return BlockFilter(allowed_faces, block_filter)

    @property
    def allowed_faces(self) -> list[BlockFace]:
        """List of any of the following strings describing which face(s) this block can be placed on: "up", "down", "north", "south", "east", "west", "side", "all". Limited to 6 faces."""
        return getattr(self, "_allowed_faces", [])

    @allowed_faces.setter
    def allowed_faces(self, value: list[BlockFace]):
        self.on_update("allowed_faces", value)
        setattr2(self, "_allowed_faces", value, list)

    @property
    def block_filter(self) -> list[BlockDescriptor]:
        """List of blocks that this block can be placed against in the "allowed_faces" direction. Limited to 64 blocks. Each block in this list can either be specified as a String (block name) or as a BlockDescriptor. A BlockDescriptor is an object that allows you to reference a block (or multiple blocks) based on its tags, or based on its name and states."""
        return getattr(self, "_block_filter", [])

    @block_filter.setter
    def block_filter(self, value: list[BlockDescriptor]):
        self.on_update("block_filter", value)
        setattr2(self, "_block_filter", value, list)

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
    """Sets rules for under what conditions the block can be placed/survive [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_placement_filter?view=minecraft-bedrock-stable)"""

    id = Identifier("placement_filter")

    def __init__(self, conditions: list[BlockFilter] = None):
        self.conditions = conditions

    def __iter__(self):
        for i in self.conditions:
            yield i

    def jsonify(self) -> dict:
        data = {"conditions": []}
        for v in self.conditions:
            data["conditions"].append(v.jsonify())
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        conditions = []
        for c in data.pop("conditions"):
            conditions.append(BlockFilter.from_dict(c))
        return PlacementFilterComponent(conditions)

    @property
    def conditions(self) -> list[BlockFilter]:
        """List of conditions where the block can be placed/survive. Limited to 64 conditions."""
        return getattr2(self, "_conditions", [])

    @conditions.setter
    def conditions(self, value: list[BlockFilter]):
        self.on_update("conditions", value)
        setattr2(self, "_conditions", value, list)

    # CONDITION

    def add_condition(self, filter: BlockFilter) -> BlockFilter:
        if not isinstance(filter, BlockFilter):
            raise TypeError(
                f"Expected Filter but got '{filter.__class__.__name__}' instead"
            )
        self.conditions.append(filter)
        return filter

    def remove_condition(self, index: int) -> BlockFilter:
        return self.conditions.pop(index)

    def clear_conditions(self) -> Self:
        self.conditions = []
        return self


@block_component_type
class QueuedTickingComponent(BlockComponent):
    """Triggers the specified event, either once, or at a regular interval equal to a number of ticks randomly chosen from the interval_range provided [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blocktriggers/minecraftblock_queued_ticking?view=minecraft-bedrock-stable)"""

    id = Identifier("queued_ticking")

    def __init__(self, interval_range: Range, on_tick: Trigger, looping: bool = None):
        self.interval_range = interval_range
        self.on_tick = on_tick
        self.looping = looping

    def jsonify(self) -> dict:
        data = {
            "interval_range": self.interval_range.to_list(),
            "on_tick": self.on_tick.jsonify(),
        }
        if self.looping is not None:
            data["looping"] = self.looping
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        interval_range = Range.from_dict(data.pop("interval_range"))
        on_tick = Trigger.from_dict(data.pop("on_tick"))
        looping = data.pop("looping") if "looping" in data else None
        return QueuedTickingComponent(interval_range, on_tick, looping)

    @property
    def interval_range(self) -> Range:
        """A range of values, specified in ticks, that will be used to decide the interval between times this event triggers. Each interval will be chosen randomly from the range, so the times between this event triggering will differ given an interval_range of two different values. If the values in the interval_range are the same, the event will always be triggered after that number of ticks."""
        return getattr(self, "_interval_range")

    @interval_range.setter
    def interval_range(self, value: Range):
        if not isinstance(value, Range):
            raise TypeError(
                f"Expected Range but got '{value.__class__.__name__}' instead"
            )
        self.on_update("interval_range", value)
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
        self.on_update("on_tick", value)
        setattr(self, "_on_tick", value)

    @property
    def looping(self) -> bool:
        """Does the event loop? If false, the event will only be triggered once, after a delay equal to a number of ticks randomly chosen from the interval_range. If true, the event will loop, and each interval between events will be equal to a number of ticks randomly chosen from the interval_range."""
        return getattr(self, "_looping", None)

    @looping.setter
    def looping(self, value: bool):
        if value is None:
            return
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("looping", value)
        setattr(self, "_looping", value)


@block_component_type
class RandomTickingComponent(BlockComponent):
    """Triggers the specified event randomly based on the random tick speed gamerule. The random tick speed determines how often blocks are updated. Some other examples of game mechanics that use random ticking are crop growth and fire spreading [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blocktriggers/minecraftblock_random_ticking?view=minecraft-bedrock-stable)"""

    id = Identifier("random_ticking")

    def __init__(self, on_tick: Trigger):
        self.on_tick = on_tick

    def jsonify(self) -> dict:
        data = {"on_tick": self.on_tick.jsonify()}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        on_tick = Trigger.from_dict(data.pop("on_tick"))
        return RandomTickingComponent(on_tick)

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
        self.on_update("on_tick", value)
        setattr(self, "_on_tick", value)


@block_component_type
class TransformationComponent(BlockComponent):
    """The block's translation, rotation and scale with respect to the center of its world position [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_transformation?view=minecraft-bedrock-stable)"""

    id = Identifier("transformation")

    def __init__(
        self,
        rotation: Vector3 = None,
        translation: Vector3 = None,
        scale: Vector3 = None,
    ):
        self.rotation = rotation
        self.translation = translation
        self.scale = scale

    @classmethod
    def rotate(cls, x: int, y: int, z: int) -> Self:
        self = cls.__new__(cls)
        self.rotation = Vector3(x, y, z)
        return self

    @classmethod
    def offset(cls, x: int, y: int, z: int) -> Self:
        self = cls.__new__(cls)
        self.translation = Vector3(x, y, z)
        return self

    @classmethod
    def scaled(cls, x: int, y: int, z: int) -> Self:
        self = cls.__new__(cls)
        self.scale = Vector3(x, y, z)
        return self

    def jsonify(self) -> dict:
        data = {}
        if self.rotation is not None:
            data["rotation"] = self.rotation.jsonify()
        if self.translation is not None:
            data["translation"] = self.translation.jsonify()
        if self.scale is not None:
            data["scale"] = self.scale.jsonify()
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        rotation = None
        translation = None
        scale = None
        if "rotation" in data:
            rotation = Vector3.from_dict(data.pop("rotation"))
        if "translation" in data:
            translation = Vector3.from_dict(data.pop("translation"))
        if "scale" in data:
            scale = Vector3.from_dict(data.pop("scale"))
        return TransformationComponent(rotation, translation, scale)

    @property
    def rotation(self) -> Vector3:
        return getattr(self, "_rotation", None)

    @rotation.setter
    def rotation(self, value: Vector3):
        if value is None:
            setattr(self, "_rotation", None)
            return
        if not isinstance(value, Vector3):
            raise TypeError(
                f"Expected Vector3 but got '{value.__class__.__name__}' instead"
            )
        self.on_update("rotation", value)
        setattr(self, "_rotation", value)

    @property
    def translation(self) -> Vector3:
        return getattr(self, "_translation", None)

    @translation.setter
    def translation(self, value: Vector3):
        if value is None:
            setattr(self, "_translation", None)
            return
        if not isinstance(value, Vector3):
            raise TypeError(
                f"Expected Vector3 but got '{value.__class__.__name__}' instead"
            )
        self.on_update("translation", value)
        setattr(self, "_translation", value)

    @property
    def scale(self) -> Vector3:
        return getattr(self, "_scale", None)

    @scale.setter
    def scale(self, value: Vector3):
        if value is None:
            setattr(self, "_scale", None)
            return
        if not isinstance(value, Vector3):
            raise TypeError(
                f"Expected Vector3 but got '{value.__class__.__name__}' instead"
            )
        self.on_update("scale", value)
        setattr(self, "_scale", value)


@block_component_type
class UnitCubeComponent(BlockComponent):
    """Specifies that a unit cube is to be used with tessellation."""

    id = Identifier("unit_cube")

    def __init__(self): ...

    def jsonify(self) -> dict:
        return {}

    @staticmethod
    def from_dict(data: dict) -> Self:
        return UnitCubeComponent()


@block_component_type
class BlockTagsComponent(BlockComponent):
    """desc"""

    id = Identifier("tags")

    def __init__(self, tags: list[Identifier] = None):
        self.tags = tags

    def jsonify(self) -> dict:
        return [str(x) for x in self.tags]

    @staticmethod
    def from_dict(data: dict) -> Self:
        tags = []
        for tag in data:
            tags.append(tag)
        return BlockTagsComponent(tags)

    @property
    def tags(self) -> list[Identifier]:
        return getattr2(self, "_tags", [])

    @tags.setter
    def tags(self, value: list[Identifiable]):
        if value is None:
            value = []
        ids = [Identifiable.of(x) for x in value]
        self.on_update("tags", ids)
        setattr2(self, "_tags", ids, list)

    def get_tag(self, index: int) -> Identifier | None:
        return getitem(self, "tags", index)

    def add_tag(self, tag: Identifiable) -> Self:
        return additem(self, "tags", Identifiable.of(tag))

    def remove_tag(self, index: int) -> Identifier:
        return removeitem(self, "tags", index)

    def clear_tags(self) -> Self:
        """Remove all tags"""
        return clearitems(self, "tags")


# TRAITS


class BlockTrait(Misc):
    def __init__(self, enabled_states: list[BlockProperty]):
        self.enabled_states = enabled_states

    def __str__(self) -> str:
        return "BlockTrait{" + str(self.id) + "}"

    def __iter__(self):
        for es in zip(*self.enabled_states):
            for s in es:
                yield s

    def __getitem__(self, index: int):
        return self.enabled_states[index]

    def jsonify(self) -> dict:
        data = {"enabled_states": [str(x.id) for x in self.enabled_states]}
        return data

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        id = Identifier.of(value)
        self.on_update("id", id)
        setattr(self, "_id", id)

    @property
    def enabled_states(self) -> list[BlockProperty]:
        """Which states to enable. Must specify at least one."""
        return getattr(self, "_enabled_states", [])

    @enabled_states.setter
    def enabled_states(self, value: list[BlockProperty]):
        if value is None:
            self.enabled_states = []
        elif isinstance(value, list):
            v = []
            for x in value:
                if not issubclass(x, BlockProperty):
                    raise TypeError(
                        f"Expected BlockProperty but got '{x.__class__.__name__}' instead"
                    )
                v.append(x())
            self.on_update("enabled_states", v)
            setattr(self, "_enabled_states", v)
        else:
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )

    @staticmethod
    def from_dict(data: dict) -> Self:
        enabled_states = None
        if "enabled_states" in data:
            enabled_states = data.pop("enabled_states")
        return BlockTrait(enabled_states)

    def generate(self, ctx) -> None:
        """
        Called when this trait is added to the Block

        :type ctx: Block
        """
        ...


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
        self, enabled_states: list[BlockProperty] = [], y_rotation_offset: float = 0.0
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

    def jsonify(self) -> dict:
        data = super().jsonify()
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
        elif value in [0.0, 90.0, 180.0, 270.0, 0, 90, 180, 270]:
            v = float(value)
            self.on_update("y_rotation_offset", v)
            setattr(self, "_y_rotation_offset", v)
        else:
            raise TypeError(
                f"Expected 0.0, 90.0, 180.0, 270.0 but got '{value.__class__.__name__}' instead"
            )

    @staticmethod
    def from_dict(data: dict) -> Self:
        enabled_states = BlockTrait.from_dict(data)
        y_rotation_offset = None
        if "y_rotation_offset" in data:
            y_rotation_offset = data.pop("y_rotation_offset")
        return PlacementDirectionTrait(enabled_states, y_rotation_offset)

    @classmethod
    def cardinal(cls, y_rotation_offset: float = 0) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([CardinalDirectionState])`
        states: ["north", "south", "east", "west"]
        """
        self = cls.__new__(cls)
        enabled_states = [CardinalDirectionState]
        BlockTrait.__init__(self, enabled_states)
        self.y_rotation_offset = y_rotation_offset
        return self

    @classmethod
    def facing(cls, y_rotation_offset: float = 0) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([FacingDirectionState])`
        states: ["down", "up", "north", "south", "east", "west"]
        """
        self = cls.__new__(cls)
        enabled_states = [FacingDirectionState]
        BlockTrait.__init__(self, enabled_states)
        self.y_rotation_offset = y_rotation_offset
        return self

    @classmethod
    def all(cls, y_rotation_offset: float = 0) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([CardinalDirectionState, FacingDirectionState])`
        """
        self = cls.__new__(cls)
        enabled_states = [CardinalDirectionState, FacingDirectionState]
        BlockTrait.__init__(self, enabled_states)
        self.y_rotation_offset = y_rotation_offset
        return self


@block_trait
class PlacementPositionTrait(BlockTrait):
    """Adds the BlockFaceState and/or VerticalHalfState BlockPropertys. The value of these state(s) are set when the block is placed."""

    id = Identifier("placement_position")

    def __init__(self, enabled_states: list[BlockProperty] = []):
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


class BlockPermutation(Misc):
    def __init__(
        self,
        condition: Molang | str,
        components: dict[Identifiable, BlockComponent] = None,
    ):
        self.condition = Molang(condition)
        self.components: dict[Identifier, BlockComponent] = components

    def __str__(self) -> str:
        return stringify(self, ["condition"])

    @staticmethod
    def from_dict(data: dict) -> Self:
        condition = Molang(data.pop("condition"))
        components = {}
        tags = BlockTagsComponent()
        for k, v in data.pop("components").items():
            id = Identifiable.of(k)
            if str(id).startswith("tag:"):
                tags.add_tag(id.path)
                continue
            clazz = INSTANCE.get_registry(Registries.BLOCK_COMPONENT_TYPE).get(id)
            if clazz is None:
                raise ComponentNotFoundError(repr(id))
            components[id] = clazz.from_dict(v)

        # Add tag
        if len(tags.tags) >= 1:
            components[Identifier("tags")] = tags
        return BlockPermutation(condition, components)

    @staticmethod
    def blockstate(prop: BlockProperty | BlockTrait, value):
        if not isinstance(prop, BlockProperty):
            raise TypeError(
                f"Expected BlockProperty but got '{prop.__class__.__name__}' instead"
            )
        return BlockPermutation(Molang(f"q.block_state('{prop.id}')=={repr(value)}"))

    def jsonify(self) -> dict:
        data = {"condition": str(self.condition), "components": {}}
        for k, v in self.components.items():
            if k == "minecraft:tags":  # Override BlockTagsComponent
                for tag in v.tags:
                    data["components"]["tag:" + str(tag)] = {}
            else:
                data["components"][str(k)] = v.jsonify()
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
        self.on_update("condition", value)
        setattr(self, "_condition", value)

    @property
    def components(self) -> dict[Identifier, BlockComponent]:
        return getattr2(self, "_components", {})

    @components.setter
    def components(self, value: dict[Identifiable, BlockComponent]):
        if value is None:
            self.components = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        components = {}
        for k, v in value.items():
            components[Identifiable.of(k)] = v
        self.on_update("components", components)
        setattr(self, "_components", components)

    def add_component(self, component: BlockComponent) -> BlockComponent:
        component.generate(self)
        return additem(self, "components", component, component.id, BlockComponent)

    def get_component(self, id: Identifiable) -> BlockComponent:
        return getitem(self, "components", Identifiable.of(id))

    def remove_component(self, id: Identifiable) -> BlockComponent:
        return removeitem(self, "components", Identifiable.of(id))

    def clear_components(self) -> Self:
        """Remove all components"""
        return clearitems(self, "components")

    def generate(self, ctx) -> None:
        """
        Called when this permutation is added to the Block

        :type ctx: Block
        """
        ...


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
    loot_table: Identifiable = None
    burnable: bool = False
    luminance: int = None
    map_color: int = None

    def color(self, color: int | MapColor) -> Self:
        if isinstance(color, MapColor):
            color = color._value_
        if isinstance(color, str):
            color = int(color.replace("#", "0x"), 16)
        if not isinstance(color, int):
            raise TypeError(
                f"Expected int but got '{color.__class__.__name__}' instead"
            )
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

    def build(self, block):
        if self.collidable is not None:
            block.add_component(CollisionBoxComponent(self.collidable))

        if self.sound_group is not None:
            block.sound_group = self.sound_group

        if self.resistance is not None:
            block.add_component(DestructibleByExplosionComponent(self.resistance))

        if self.hardness is not None:
            block.add_component(DestructibleByMiningComponent(self.hardness))

        if self.slipperiness is not None:
            block.add_component(FrictionComponent(self.slipperiness))

        if self.loot_table is not None:
            block.add_component(LootComponent(self.loot_table))

        # use molang?
        if self.luminance is not None:
            block.add_component(LightEmissionComponent(self.luminance))

        if self.map_color is not None:
            block.add_component(MapColorComponent(self.map_color))

        if self.burnable:
            block.add_component(FlammableComponent(0, 0))
        return block


class BlockState(Misc):
    """
    Describes a placed block in the world
    """

    def __init__(self, name: Identifiable, states: dict = None):
        self.name = name
        self.states = states

    def __str__(self) -> str:
        return "BlockState{" + str(self.name) + "}"

    @property
    def name(self) -> Identifier:
        return getattr(self, "_name")

    @name.setter
    def name(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("name", id)
        setattr(self, "_name", id)

    @property
    def states(self) -> dict:
        return getattr2(self, "_states", {})

    @states.setter
    def states(self, value: dict[Identifiable, str]):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        states = {}
        for k, v in value.items():
            states[Identifiable.of(k)] = v
        self.on_update("states", states)
        setattr(self, "_states", states)

    @staticmethod
    def of(value) -> Self:
        if isinstance(value, BlockState):
            return value
        elif isinstance(value, Block):
            return value.defaultstate()
        elif isinstance(value, dict):
            return BlockState.from_dict(value)
        return BlockState(value, {})

    @staticmethod
    def from_dict(data: dict) -> Self:
        if isinstance(data, str):
            return BlockState(data)
        return BlockState(**data)

    def jsonify(self) -> dict:
        if not self.has_states():
            return str(self.name)

        states = {}
        for k, v in self.states.items():
            states[str(k)] = v
        data = {"name": str(self.name), "states": states}
        return data

    def has_states(self) -> bool:
        return len(self.states) >= 1


class BlockPredicate(Misc):
    """
    Describes a block predicate that should match. Similar to BlockState but excepts "tags"
    """

    def __init__(self, name: str = None, states: dict = None, tags: Molang = None):
        self.name = name
        self.tags = tags
        self.states = states

    def __str__(self) -> str:
        return "BlockPredicate{" + str(self.name) if self.name else self.tags + "}"

    @property
    def name(self) -> Identifier:
        return getattr(self, "_name", None)

    @name.setter
    def name(self, value: Identifiable):
        if value is None:
            return
        id = Identifiable.of(value)
        self.on_update("name", id)
        setattr(self, "_name", id)

    @property
    def states(self) -> dict:
        return getattr2(self, "_states", {})

    @states.setter
    def states(self, value: dict[Identifiable, str]):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        states = {}
        for k, v in value.items():
            states[Identifiable.of(k)] = v
        self.on_update("states", states)
        setattr(self, "_states", states)

    @property
    def tags(self) -> Molang:
        return getattr(self, "_tags", None)

    @tags.setter
    def tags(self, value: Molang):
        if value is None:
            return
        if not isinstance(value, (Molang, str)):
            raise TypeError(
                f"Expected Molang, str but got '{value.__class__.__name__}' instead"
            )
        v = Molang(value)
        self.on_update("tags", v)
        setattr(self, "_tags", v)

    @staticmethod
    def of(value) -> Self:
        if isinstance(value, BlockPredicate):
            return value
        elif isinstance(value, BlockState):
            return BlockPredicate(value.name, value.states)
        elif isinstance(value, Block):
            return BlockPredicate.of(value.defaultstate())
        elif isinstance(value, Molang):
            return BlockPredicate(tags=value)
        elif isinstance(value, dict):
            return BlockPredicate.from_dict(value)
        return BlockPredicate(value, {})

    @staticmethod
    def from_dict(data: dict) -> Self:
        if isinstance(data, str):
            return BlockPredicate(data)
        return BlockPredicate(**data)

    def jsonify(self) -> dict:
        if not self.has_states():
            return str(self.name) if self.name else str(self.tags)

        states = {}
        for k, v in self.states.items():
            states[str(k)] = v
        data = {"states": states}
        if self.name:
            data["name"] = str(self.name)
        else:
            data["tags"] = str(self.tags)
        return data

    def has_states(self) -> bool:
        return len(self.states) >= 1


@resource_pack
@behavior_pack
class Block(JsonFile, Identifiable):
    """
    Represents a data-driven Block. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockjsonfilestructure?view=minecraft-bedrock-stable)
    """

    id = Identifier("block")
    FILEPATH = "blocks/block.json"

    def __init__(
        self,
        identifier: Identifiable,
        menu_category: MenuCategory = None,
        components: dict[str, BlockComponent] = None,
        permutations: list[BlockPermutation] = None,
        events: dict[Identifiable, Event] = None,
        traits: dict[Identifiable, BlockTrait] = None,
        states: dict[Identifiable, list[str]] = None,
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

    @property
    def type(self) -> Identifier:
        return getattr(self, "_type", None)

    @type.setter
    def type(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("type", id)
        setattr(self, "_type", id)

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
        self.on_update("menu_category", value)
        setattr(self, "_menu_category", value)

    @property
    def components(self) -> dict[str, BlockComponent]:
        return getattr2(self, "_components", {})

    @components.setter
    def components(self, value: dict[str, BlockComponent]):
        self.on_update("components", value)
        setattr2(self, "_components", value, dict)

    @property
    def permutations(self) -> list[BlockPermutation]:
        return getattr2(self, "_permutations", [])

    @permutations.setter
    def permutations(self, value: list[BlockPermutation]):
        self.on_update("permutations", value)
        setattr2(self, "_permutations", value, list)

    @property
    def events(self) -> dict[Identifier, Event]:
        return getattr2(self, "_events", {})

    @events.setter
    def events(self, value: dict[Identifiable, Event]):
        if value is None:
            self.events = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        events = {}
        for k, v in value.items():
            events[Identifiable.of(k)] = v
        self.on_update("events", events)
        setattr(self, "_events", events)

    @property
    def states(self) -> dict[Identifier, BlockProperty]:
        return getattr2(self, "_states", {})

    @states.setter
    def states(self, value: dict[Identifiable, BlockProperty]):
        if value is None:
            self.states = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        states = {}
        for k, v in value.items():
            states[Identifiable.of(k)] = v
        self.on_update("states", states)
        setattr(self, "_states", states)

    @property
    def traits(self) -> dict[Identifier, BlockTrait]:
        return getattr2(self, "_traits", {})

    @traits.setter
    def traits(self, value: dict[Identifiable, BlockTrait]):
        if value is None:
            self.traits = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        traits = {}
        for k, v in value.items():
            traits[Identifiable.of(k)] = v
        self.on_update("traits", traits)
        setattr(self, "_traits", traits)

    @property
    def sound_group(self) -> str | None:
        return getattr(self, "_sound_group", None)

    @sound_group.setter
    def sound_group(self, value: str | None):
        if value is None:
            setattr(self, "_sound_group", None)
            return
        v = str(value)
        self.on_update("sound_group", v)
        setattr(self, "_sound_group", v)

    @property
    def name(self) -> str | None:
        return getattr(self, "_name", None)

    @name.setter
    def name(self, value: str):
        setattr(self, "_name", str(value))

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

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = BlockLoader()
        loader.validate(data)
        return loader.load(data)

    @classmethod
    def from_settings(cls, identifier: Identifiable, settings: BlockSettings) -> Self:
        """
        Create a block using block settings

        :param identifier: The ID of the block
        :type identifier: Identifiable
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
        return settings.build(self)

    def jsonify(self) -> dict:
        block = {"description": {"identifier": str(self.identifier)}}
        if self.menu_category:
            block["description"]["menu_category"] = self.menu_category.jsonify()

        if self.traits:
            block["description"]["traits"] = {}
            for k, v in self.traits.items():
                block["description"]["traits"][str(k)] = v.jsonify()

        if self.states:
            block["description"]["states"] = {}
            for k, v in self.states.items():
                block["description"]["states"].update(v.jsonify())

        if self.components:
            block["components"] = {}
            for k, v in self.components.items():
                if k == "minecraft:tags":  # Override BlockTagsComponent
                    for tag in v.tags:
                        block["components"]["tag:" + str(tag)] = {}
                else:
                    block["components"][str(k)] = v.jsonify()

        if self.permutations:
            block["permutations"] = []
            for v in self.permutations:
                block["permutations"].append(v.jsonify())

        if self.events:
            block["events"] = {}
            for key, events in self.events.items():
                d = {}
                for k, v in events.items():
                    d[k.path] = v.jsonify()
                block["events"][str(key)] = d

        data = {"format_version": VERSION["BLOCK"], str(self.id): block}
        if self.type:
            data["type"] = str(self.type)
        return data

    def display_name(self, text: str) -> Self:
        """
        The name of this block in-game.

        :rtype: Self
        """
        self.name = text
        return self

    def defaultstate(self) -> BlockState:
        """
        This blocks default BlockState

        :rtype: BlockState
        """
        states = {}
        for id, state in self.states.items():
            states[id] = state.default()
        return BlockState(self.identifier, states)

    def translation_key(self) -> str:
        return f"tile.{self.identifier}.name"

    def stack(self):
        from .item import ItemStack

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

    def generate(self, ctx) -> None:
        """
        Called when this block is added to ResourcePack or BehaviorPack

        :type ctx: ResourcePack | BehaviorPack
        """
        for e in self.events.values():
            for et in e.values():
                et.generate(ctx)
        for t in self.traits.values():
            t.generate(ctx)
        for p in self.permutations:
            p.generate(ctx)
        for c in self.components.values():
            c.generate(ctx)
        if isinstance(ctx, ResourcePack) and self.name is not None:
            ctx.texts[self.translation_key()] = self.name

    def item(self, id: Identifiable, icon: Identifiable = None, *args, **kw):
        from .item import BlockItem

        return BlockItem(
            self.identifier.replace("_block", "") if id is None else id,
            self,
            self.identifier if icon is None else icon,
            *args,
            **kw,
        ).display_name(self.name)

    # COMPONENT

    def add_component(self, component: BlockComponent) -> BlockComponent:
        if not isinstance(component, BlockComponent):
            raise TypeError(
                f"Expected BlockComponent but got '{component.__class__.__name__}' instead"
            )
        if isinstance(component, Trigger):
            component.event.namespace = self.identifier.namespace
        component.generate(self)
        self.components[component.id] = component
        return additem(self, "components", component, component.id, BlockComponent)

    def get_component(self, id: Identifiable) -> BlockComponent:
        return getitem(self, "components", Identifiable.of(id))

    def remove_component(self, id: str) -> BlockComponent:
        return removeitem(self, "components", Identifiable.of(id))

    def clear_components(self) -> Self:
        """Removes all components"""
        return clearitems(self, "components")

    # EVENT
    def _event_id(self, id: Identifier | str):
        if id is None:
            return Identifier("default")
        elif isinstance(id, Identifier):
            return id
        else:
            return self.identifier.copy_with_path(id)

    def add_event(self, id: Identifiable, event: Event) -> Event:
        if isinstance(event, Event):
            k = self._event_id(id)
            if k in self.events:
                event.generate(self)
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

    def add_events(self, id: Identifiable, *events: Event) -> list[Event]:
        return [self.add_event(id, e) for e in events]

    def get_event(self, id: Identifiable) -> Event:
        k = self._event_id(id)
        return self.events.get(k)

    def remove_event(self, id: Identifiable) -> Event:
        return removeitem(self, "events", Identifiable.of(id))

    def clear_events(self) -> Self:
        """Removes all events"""
        return clearitems(self, "events")

    # PERMUTATION

    def add_permutation(self, permutation: BlockPermutation) -> BlockPermutation:
        if not isinstance(permutation, BlockPermutation):
            raise TypeError(
                f"Expected BlockPermutation but got '{permutation.__class__.__name__}' instead"
            )
        permutation.generate(self)
        return additem(self, "permutations", permutation)

    def add_permutations(
        self, *permutations: BlockPermutation
    ) -> list[BlockPermutation]:
        return [self.add_permutation(perm) for perm in permutations]

    def get_permutation(self, index: int) -> BlockPermutation:
        return self.permutations[index]

    def remove_permutation(self, index: int) -> BlockPermutation:
        return removeitem(self, "permutations", index)

    def clear_permutation(self) -> Self:
        """Removes all permutations"""
        return clearitems(self, "permutations")

    # TRAIT

    def add_trait(self, trait: BlockTrait) -> BlockTrait:
        if not isinstance(trait, BlockTrait):
            raise TypeError(
                f"Expected BlockTrait but got '{trait.__class__.__name__}' instead"
            )
        trait.generate(self)
        self.traits[trait.id] = trait
        return trait

    def add_traits(self, *traits: BlockTrait) -> list[BlockTrait]:
        return [self.add_trait(trait) for trait in traits]

    def get_trait(self, id: Identifiable) -> BlockTrait:
        return getitem(self, "traits", Identifiable.of(id))

    def remove_trait(self, id: Identifiable) -> BlockTrait:
        return removeitem(self, "traits", Identifiable.of(id))

    def clear_trait(self) -> Self:
        """Removes all traits"""
        return clearitems(self, "traits")

    # STATE

    def add_state(self, state: BlockProperty) -> BlockProperty:
        if not isinstance(state, BlockProperty):
            raise TypeError(
                f"Expected BlockProperty but got '{state.__class__.__name__}' instead"
            )
        self.states[state.id] = state
        return state

    def get_state(self, id: Identifiable) -> BlockProperty:
        return getitem(self, "states", Identifiable.of(id))

    def remove_state(self, id: Identifiable) -> BlockProperty:
        return removeitem(self, "states", Identifiable.of(id))

    def clear_state(self) -> Self:
        """Removes all states"""
        return clearitems(self, "states")


class BlockLoader(Loader):
    name = "Block"

    def __init__(self):
        from .schemas import BlockSchema1

        Loader.__init__(self, Block)
        self.add_schema(BlockSchema1, "1.20.50")


# TYPES

INSTANCE.create_registry(Registries.BLOCK_TYPE, Block)


def block_type(cls):
    """
    Add this block type to the registry
    """

    def wrapper():
        return INSTANCE.register(Registries.BLOCK_TYPE, cls.type, cls)

    return wrapper()
