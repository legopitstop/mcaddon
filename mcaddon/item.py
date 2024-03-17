from typing import Self
from dataclasses import dataclass
import json

from . import VERSION
from .constant import UseAnimation
from .registry import INSTANCE, Registries
from .file import JsonFile, Loader
from .pack import behavior_pack, resource_pack, ResourcePack
from .util import (
    getattr2,
    getitem,
    additem,
    removeitem,
    clearitems,
    Identifier,
    MenuCategory,
    Identifiable,
    Misc,
)
from .event import Event
from .block import BlockDescriptor


# COMPONENTS


class ItemComponent(Misc):
    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return "ItemComponent{" + str(self.id) + "}"

    def __call__(self, ctx) -> int:
        return self.execute(ctx)

    def jsonify(self) -> dict:
        raise NotImplementedError()

    def json(self) -> str:
        return json.dumps(self.jsonify())

    @staticmethod
    def from_dict(data: dict) -> Self:
        raise NotImplementedError()

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier.of(value))

    def execute(self, ctx) -> int:
        return 0

    def generate(self, ctx) -> None:
        """
        Called when this component is added to an Item

        :type ctx: Item
        """
        ...


class SimpleItemComponent(ItemComponent):
    def __init__(self, value):
        self.value = value

    def jsonify(self):
        data = self.value
        return data

    @property
    def value(self):
        return getattr(self, "_value")

    @value.setter
    def value(self, value):
        if not isinstance(self.clazz, tuple) and issubclass(self.clazz, Identifiable):
            setattr(self, "_value", Identifiable.of(value))
        else:
            if isinstance(value, self.clazz):
                self.on_update("value", value)
                setattr(self, "_value", value)
            else:
                raise TypeError(
                    f"Expected {self.clazz.__name__} but got '{value.__class__.__name__}' instead"
                )


class EmptyItemComponent(ItemComponent):
    def jsonify(self):
        data = {}
        return data

    @classmethod
    def from_dict(cls, data) -> Self:
        self = cls.__new__(cls)
        return self


INSTANCE.create_registry(Registries.ITEM_COMPONENT_TYPE, ItemComponent)


def item_component_type(cls):
    """
    Add this item component to the registry
    """

    def wrapper():
        if not issubclass(cls, ItemComponent):
            raise TypeError(f"Expected ItemComponent but got '{cls.__name__}' instead")
        return INSTANCE.register(Registries.ITEM_COMPONENT_TYPE, cls.id, cls)

    return wrapper()


# 1.20.51


@item_component_type
class IgnoresPermissionComponent(SimpleItemComponent):
    """ """

    id = Identifier("ignores_permission")
    clazz = bool

    @staticmethod
    def from_dict(data: bool) -> Self:
        return IgnoresPermissionComponent(data)


@item_component_type
class AllowOffHandComponent(SimpleItemComponent):
    """The allow off hand component determines whether the item can be placed in the off hand slot of the inventory. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_allow_off_hand?view=minecraft-bedrock-stable)"""

    id = Identifier("allow_off_hand")
    clazz = bool

    @staticmethod
    def from_dict(data: bool) -> Self:
        return AllowOffHandComponent(data)


@item_component_type
class BlockPlacerComponent(ItemComponent):
    """Block Placer item component. Items with this component will place a block when used. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_block_placer?view=minecraft-bedrock-stable)"""

    id = Identifier("block_placer")

    def __init__(self, block: Identifiable, use_on: list[BlockDescriptor] = []):
        self.block = block
        self.use_on = use_on

    def jsonify(self) -> dict:
        data = {"block": str(self.block)}
        if self.use_on:
            data["use_on"] = [x.jsonify() for x in self.use_on]
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        block = data.pop("block")
        use_on = []
        if "use_on" in data:
            use_on = data.pop("use_on")
        return BlockPlacerComponent(block, use_on)

    @property
    def block(self) -> Identifier:
        """Defines the block that will be placed."""
        return getattr(self, "_block")

    @block.setter
    def block(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("block", id)
        setattr(self, "_block", id)

    @property
    def use_on(self) -> list[BlockDescriptor]:
        """List of block descriptors that contain blocks that this item can be used on. If left empty, all blocks will be allowed."""
        return getattr2(self, "_use_on", [])

    @use_on.setter
    def use_on(self, value: list[BlockDescriptor]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("use_on", value)
        setattr(self, "_use_on", value)

    def get_use_on(self, index: int) -> BlockDescriptor:
        return getitem(self, "use_on", index)

    def add_use_on(self, block: BlockDescriptor) -> BlockDescriptor:
        return additem(self, "use_on", block, type=BlockDescriptor)

    def remove_use_on(self, index: int) -> BlockDescriptor:
        return removeitem(self, "use_on", index)

    def clear_use_on(self) -> Self:
        """Remove all use on blocks"""
        return clearitems(self, "use_on")


@item_component_type
class CanDestroyInCreativeComponent(SimpleItemComponent):
    """The can destroy in creative component determines if the item will break blocks in creative when swinging. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_can_destroy_in_creative?view=minecraft-bedrock-stable)"""

    id = Identifier("can_destroy_in_creative")
    clazz = bool

    @staticmethod
    def from_dict(data: bool) -> Self:
        return CanDestroyInCreativeComponent(data)


@item_component_type
class CooldownComponent(ItemComponent):
    """Cool down time for a component. After you use an item, all items specified with the same `cool down category` setting becomes unusable for the duration specified by the 'cool down time' setting in this component. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_cooldown?view=minecraft-bedrock-stable)"""

    id = Identifier("cooldown")

    def __init__(self, category: str, duration: float):
        self.category = category
        self.duration = duration

    def jsonify(self) -> dict:
        data = {"category": self.category, "duration": self.duration}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return CooldownComponent(**data)

    @property
    def category(self) -> str:
        """The type of cool down for this item. All items with a cool down component with the same category are put on cool down when one is used."""
        return getattr(self, "_category")

    @category.setter
    def category(self, value: str):
        v = str(value)
        self.on_update("category", v)
        setattr(self, "_category", v)

    @property
    def duration(self) -> float:
        """The duration of time (in seconds) items with a matching category will spend cooling down before becoming usable again."""
        return getattr(self, "_duration")

    @duration.setter
    def duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("duration", v)
        setattr(self, "_duration", v)


@item_component_type
class DamageComponent(ItemComponent):
    """
    The damage component determines how much extra damage the item does on attack. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_damage?view=minecraft-bedrock-stable)
    """

    id = Identifier("damage")
    clazz = int

    def __init__(self, value: int):
        self.value = value

    def jsonify(self) -> dict:
        data = {"value": self.value}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return DamageComponent(**data)


@item_component_type
class ItemDisplayNameComponent(ItemComponent):
    """
    Display Name item component. Determines the text shown whenever an item's name is displayed (ex. hover text). [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_display_name?view=minecraft-bedrock-stable)
    """

    id = Identifier("display_name")

    def __init__(self, value: str):
        self.value = value

    def jsonify(self) -> dict:
        data = {"value": self.value}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return ItemDisplayNameComponent(**data)

    @property
    def value(self) -> str:
        return getattr(self, "_value")

    @value.setter
    def value(self, value: str):
        v = str(value)
        self.on_update("value", v)
        setattr(self, "_value", v)


@item_component_type
class DurabilityComponent(ItemComponent):
    """
    Durability item component. Determines how much damage this item takes before breaking and allows the item to be combined in crafting. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_durability?view=minecraft-bedrock-stable)
    """

    id = Identifier("durability")

    def __init__(self, damage_chance: float, max_durability: int):
        self.damage_chance = damage_chance
        self.max_durability = max_durability

    def jsonify(self) -> dict:
        data = {
            "damage_chance": self.damage_chance,
            "max_durability": self.max_durability,
        }
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return DurabilityComponent(**data)

    @property
    def damage_chance(self) -> float:
        """Damage chance is the percentage chance of this item losing durability. Default is set to 100. Defined as an int range with min and max value."""
        return getattr(self, "_damage_chance")

    @damage_chance.setter
    def damage_chance(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("damage_chance", v)
        setattr(self, "_damage_chance", v)

    @property
    def max_durability(self) -> int:
        """Max durability is the amount of damage that this item can take before breaking. This is a required parameter and has a minimum of 0."""
        return getattr(self, "_max_durability")

    @max_durability.setter
    def max_durability(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("max_durability", value)
        setattr(self, "_max_durability", value)


@item_component_type
class EnchantableComponent(ItemComponent):
    """
    The enchantable component determines what enchantments can be applied to the item. Not all enchantments will have an effect on all item components. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_enchantable?view=minecraft-bedrock-stable)
    """

    id = Identifier("enchantable")

    def __init__(self, slot: str, value: int):
        self.slot = slot
        self.value = value

    def jsonify(self) -> dict:
        data = {"slot": self.slot, "value": self.value}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return EnchantableComponent(**data)

    @property
    def slot(self) -> str:
        """What enchantments can be applied (ex. Using `bow` would allow this item to be enchanted as if it were a bow)."""
        return getattr(self, "_slot")

    @slot.setter
    def slot(self, value: str):
        v = str(value)
        self.on_update("slot", v)
        setattr(self, "_slot", v)

    @property
    def value(self) -> int:
        """The value of the enchantment (minimum of 0)."""
        return getattr(self, "_value")

    @value.setter
    def value(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("value", value)
        setattr(self, "_value", value)


@item_component_type
class EntityPlacerComponent(ItemComponent):
    """
    Entity placer item component. You can specifiy allowed blocks that the item is restricted to. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_entity_placer?view=minecraft-bedrock-stable)
    """

    id = Identifier("entity_placer")

    def __init__(self, entity: Identifiable, dispense_on: list = [], use_on: list = []):
        self.entity = entity
        self.dispense_on = dispense_on
        self.use_on = use_on

    def jsonify(self) -> dict:
        data = {"entity": str(self.entity)}
        if self.dispense_on:
            data["dispense_on"] = self.dispense_on
        if self.use_on:
            data["use_on"] = self.use_on
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        entity = data.pop("entity")
        dispense_on = data.pop("dispense_on") if "dispense_on" in data else []
        use_on = data.pop("use_on") if "use_on" in data else []
        return EntityPlacerComponent(entity, dispense_on, use_on)

    @property
    def entity(self) -> Identifier:
        """The entity to be placed in the world."""
        return getattr(self, "_entity")

    @entity.setter
    def entity(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("entity", id)
        setattr(self, "_entity", id)

    @property
    def dispense_on(self) -> list:
        """List of block descriptors that contain blocks that this item can be dispensed on. If left empty, all blocks will be allowed., defaults to None"""
        return getattr2(self, "_dispense_on", [])

    @dispense_on.setter
    def dispense_on(self, value: list):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("dispense_on", value)
        setattr(self, "_dispense_on", value)

    @property
    def use_on(self) -> list:
        """List of block descriptors that contain blocks that this item can be used on. If left empty, all blocks will be allowed., defaults to None"""
        return getattr2(self, "_use_on", [])

    @use_on.setter
    def use_on(self, value: list):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("use_on", value)
        setattr(self, "_use_on", value)

    def get_dispense_on(self, index: int) -> BlockDescriptor:
        return getitem(self, "dispense_on", index)

    def add_dispense_on(self, block: BlockDescriptor) -> BlockDescriptor:
        return additem(self, "dispense_on", block, type=BlockDescriptor)

    def remove_dispense_on(self, index: int) -> BlockDescriptor:
        return removeitem(self, "dispense_on", index)

    def clear_dispense_on(self) -> Self:
        return clearitems(self, "dispense_on")

    def get_use_on(self, index: int) -> BlockDescriptor:
        return getitem(self, "use_on", index)

    def add_use_on(self, block: BlockDescriptor) -> BlockDescriptor:
        return additem(self, "use_on", block, type=BlockDescriptor)

    def remove_use_on(self, index: int) -> BlockDescriptor:
        return removeitem(self, "use_on", index)

    def clear_use_on(self) -> Self:
        return clearitems(self, "use_on")


@item_component_type
class FoodComponent(ItemComponent):
    """
    When an item has a food component, it becomes edible to the player. Must have the 'minecraft:use_duration' component in order to function properly. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_food?view=minecraft-bedrock-stable)
    """

    id = Identifier("food")

    def __init__(
        self,
        nutrition: int,
        saturation_modifier: float = None,
        can_always_eat: bool = False,
        using_converts_to: Identifiable = None,
        is_meat: bool = False,
    ):
        self.nutrition = nutrition
        self.saturation_modifier = saturation_modifier
        self.can_always_eat = can_always_eat
        self.using_converts_to = using_converts_to
        self.is_meat = is_meat

    def jsonify(self) -> dict:
        data = {}
        if self.nutrition is not None:
            data["nutrition"] = self.nutrition
        if self.saturation_modifier not in [None, 0.6]:
            data["saturation_modifier"] = self.saturation_modifier
        if self.can_always_eat is not False:
            data["can_always_eat"] = self.can_always_eat
        if self.using_converts_to is not None:
            data["using_converts_to"] = str(self.using_converts_to)
        if self.is_meat not in [None, False]:
            data["is_meat"] = self.is_meat
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        for x in [
            "effects",
            "on_use_action",
            "on_use_range",
            "cooldown_type",
            "cooldown_time",
            "remove_effects",
        ]:
            if x in data:
                del data[x]
        return FoodComponent(**data)

    @property
    def is_meat(self) -> bool:
        return getattr(self, "_is_meat")

    @is_meat.setter
    def is_meat(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("is_meat", value)
        setattr(self, "_is_meat", value)

    @property
    def nutrition(self) -> int:
        """The value that is added to the actor's nutrition when the item is used. Default is set to 0."""
        return getattr(self, "_nutrition")

    @nutrition.setter
    def nutrition(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("nutrition", value)
        setattr(self, "_nutrition", value)

    @property
    def saturation_modifier(self) -> float:
        """Saturation Modifier is used in this formula: (nutrition * saturation_modifier * 2) when applying the saturation buff. Default is set to 0.6., defaults to None"""
        return getattr(self, "_saturation_modifier", 0.6)

    @saturation_modifier.setter
    def saturation_modifier(self, value: float):
        if value is None:
            self.saturation_modifier = 0.6
            return
        if isinstance(value, str):
            # Values are from Java Edition https://maven.fabricmc.net/docs/yarn-1.20.4+build.1/net/minecraft/item/FoodComponents.html
            match value:
                case "poor":
                    self.saturation_modifier = 0.1
                case "low":
                    self.saturation_modifier = 0.3
                case "normal":
                    self.saturation_modifier = 0.6
                case "good":
                    self.saturation_modifier = 0.8
                case "supernatural":
                    self.saturation_modifier = 1.2
                case _:
                    raise ValueError(value)
            return
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("saturation_modifier", v)
        setattr(self, "_saturation_modifier", v)

    @property
    def can_always_eat(self) -> bool:
        """If true you can always eat this item (even when not hungry). Default is set to false., defaults to False"""
        return getattr(self, "_can_always_eat", False)

    @can_always_eat.setter
    def can_always_eat(self, value: bool):
        if value is None:
            value = False
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("can_always_eat", value)
        setattr(self, "_can_always_eat", value)

    @property
    def using_converts_to(self) -> Identifier | None:
        """When used, converts to the item specified by the string in this field. Default does not convert item., defaults to None"""
        return getattr(self, "_using_converts_to", None)

    @using_converts_to.setter
    def using_converts_to(self, value: Identifiable | None):
        if value is None:
            setattr(self, "_using_converts_to", None)
        else:
            id = Identifiable.of(value)
            self.on_update("using_converts_to", id)
            setattr(self, "_using_converts_to", id)


@item_component_type
class FuelComponent(ItemComponent):
    """
    Fuel item component. Allows this item to be used as fuel in a furnace to 'cook' other items. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_fuel?view=minecraft-bedrock-stable)
    """

    id = Identifier("fuel")

    def __init__(self, duration: float):
        self.duration = duration

    def jsonify(self) -> dict:
        data = {"duration": self.duration}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return FuelComponent(**data)

    @property
    def duration(self) -> float:
        """How long in seconds will this fuel cook items for."""
        return getattr(self, "_duration")

    @duration.setter
    def duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("duration", v)
        setattr(self, "_duration", v)


@item_component_type
class GlintComponent(SimpleItemComponent):
    """
    The glint component determines whether the item has the enchanted glint render effect on it. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_glint?view=minecraft-bedrock-stable)
    """

    id = Identifier("glint")
    clazz = bool

    def jsonify(self) -> dict:
        data = self.value
        return data

    @staticmethod
    def from_dict(data: bool) -> Self:
        return GlintComponent(data)


@item_component_type
class HandEquippedComponent(SimpleItemComponent):
    """
    This component determines if an item is rendered like a tool while in hand. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_hand_equipped?view=minecraft-bedrock-stable)
    """

    id = Identifier("hand_equipped")
    clazz = bool

    @staticmethod
    def from_dict(data: bool) -> Self:
        return HandEquippedComponent(data)


@item_component_type
class HoverTextColorComponent(SimpleItemComponent):
    """
    The hover text color component determines the color of the item name when hovering over it. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_hover_text_color?view=minecraft-bedrock-stable)
    """

    id = Identifier("hover_text_color")
    clazz = str

    def jsonify(self) -> dict:
        data = {"value": self.value}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return HoverTextColorComponent(**data)


@item_component_type
class IconComponent(ItemComponent):
    """
    Icon item component. Determines the icon to represent the item in the UI and elsewhere. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_icon?view=minecraft-bedrock-stable)
    """

    id = Identifier("icon")

    def __init__(self, texture: Identifiable):
        self.texture = texture

    def jsonify(self) -> dict:
        data = {"texture": str(self.texture)}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return IconComponent(**data)

    @property
    def texture(self) -> Identifier:
        """The key from the resource_pack/textures/item_texture.json 'texture_data' object associated with the texture file."""
        return getattr(self, "_texture")

    @texture.setter
    def texture(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("texture", id)
        setattr(self, "_texture", id)


@item_component_type
class InteractButtonComponent(SimpleItemComponent):
    """
    This component is a boolean or string that determines if the interact button is shown in touch controls and what text is displayed on the button. When set as true, default "Use Item" text will be used.z [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_interact_button?view=minecraft-bedrock-stable)
    """

    id = Identifier("interact_button")
    clazz = (str, bool)

    def jsonify(self) -> dict:
        data = {"value": self.value}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return InteractButtonComponent(**data)


@item_component_type
class ItemStorageComponent(ItemComponent):
    """
    The Storage Item Component is used for storing Items within an Item's User Data
    """

    id = Identifier("item_storage")

    def __init__(self, capacity: int):
        self.capacity = capacity

    def jsonify(self) -> dict:
        data = {"capacity": self.capacity}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return ItemStorageComponent(**data)

    @property
    def capacity(self) -> int:
        """The max capacity of the item, default is 64"""
        return getattr(self, "_capacity")

    @capacity.setter
    def capacity(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("capacity", value)
        setattr(self, "_capacity", value)


@item_component_type
class LiquidClippedComponent(SimpleItemComponent):
    """
    The liquid clipped component determines whether the item interacts with liquid blocks on use. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_liquid_clipped?view=minecraft-bedrock-stable)
    """

    id = Identifier("liquid_clipped")
    clazz = bool

    def jsonify(self) -> dict:
        data = {"value": self.value}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return LiquidClippedComponent(**data)


@item_component_type
class MaxStackSizeComponent(SimpleItemComponent):
    """
    The max stack size component determines how many of the item can be stacked together. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_max_stack_size?view=minecraft-bedrock-stable)
    """

    id = Identifier("max_stack_size")
    clazz = int

    @staticmethod
    def from_dict(data: int) -> Self:
        return MaxStackSizeComponent(data)


@item_component_type
class ProjectileComponent(ItemComponent):
    """
    Projectile item component. projectile items shoot out, like an arrow. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_projectile?view=minecraft-bedrock-stable)
    """

    id = Identifier("projectile")

    def __init__(self, projectile_entity: Identifiable, minimum_critical_power: float):
        self.projectile_entity = projectile_entity
        self.minimum_critical_power = minimum_critical_power

    def jsonify(self) -> dict:
        data = {
            "projectile_entity": str(self.projectile_entity),
            "minimum_critical_power": self.minimum_critical_power,
        }
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return ProjectileComponent(**data)

    @property
    def projectile_entity(self) -> Identifier:
        """How long you must charge a projectile for it to critically hit."""
        return getattr(self, "_projectile_entity")

    @projectile_entity.setter
    def projectile_entity(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("projectile_entity", id)
        setattr(self, "_projectile_entity", id)

    @property
    def minimum_critical_power(self) -> float:
        """The entity to be fired as a projectile."""
        return getattr(self, "_minimum_critical_power")

    @minimum_critical_power.setter
    def minimum_critical_power(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("minimum_critical_power", v)
        setattr(self, "_minimum_critical_power", v)


@item_component_type
class RecordComponent(ItemComponent):
    """
    Record Item Component. Used by record items to play music. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_record?view=minecraft-bedrock-stable)
    """

    id = Identifier("record")

    def __init__(
        self, comparator_signal: int, duration: float, sound_event: Identifiable
    ):
        self.comparator_signal = comparator_signal
        self.duration = duration
        self.sound_event = sound_event

    def jsonify(self) -> dict:
        data = {
            "comparator_signal": self.comparator_signal,
            "duration": self.duration,
            "sound_event": str(self.sound_event),
        }
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return RecordComponent(**data)

    @property
    def comparator_signal(self) -> int:
        """Signal strength for comparator blocks to use, from 1 - 13."""
        return getattr(self, "_comparator_signal")

    @comparator_signal.setter
    def comparator_signal(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("comparator_signal", value)
        setattr(self, "_comparator_signal", value)

    @property
    def duration(self) -> float:
        """Duration of sound event in seconds, float value."""
        return getattr(self, "_duration")

    @duration.setter
    def duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("duration", v)
        setattr(self, "_duration", v)

    @property
    def sound_event(self) -> Identifier:
        """Sound event type: 13, cat, blocks, chirp, far, mall, mellohi, stal, strad, ward, 11, wait, pigstep, otherside, 5, relic."""
        return getattr(self, "_sound_event")

    @sound_event.setter
    def sound_event(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("sound_event", id)
        setattr(self, "_sound_event", id)


class RepairItem:
    @staticmethod
    def from_dict(data: dict) -> Self:
        return RepairItem(**data)

    def to_dict(self) -> dict:
        data = {}
        return data


@item_component_type
class RepairableComponent(ItemComponent):
    """
    Repairable item component. Determines the items that can be used to repair this item along with how much durability they repair. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_repairable?view=minecraft-bedrock-stable)
    """

    id = Identifier("repairable")

    def __init__(self, repair_items: list[RepairItem] = None):
        self.repair_items = repair_items

    def jsonify(self) -> dict:
        data = {"repair_items": [x.jsonify() for x in self.repair_items]}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return RepairableComponent(
            [RepairItem.from_dict(x) for x in data.pop("repair_items")]
        )

    @property
    def repair_items(self) -> list[RepairItem]:
        """List of repair item entries. Each entry needs to define a list of strings for `items` that can be used for the repair and an optional `repair_amount` for how much durability is repaired., defaults to None"""
        return getattr(self, "_repair_items", [])

    @repair_items.setter
    def repair_items(self, value: list[RepairItem]):
        if value is None:
            self.repair_items = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("repair_items", value)
        setattr(self, "_repair_items", value)

    def get_repair_item(self, index: int) -> RepairItem:
        return getitem(self, "repair_items", index)

    def add_repair_item(self, item: RepairItem) -> RepairItem:
        return additem(self, "repair_items", item, type=RepairItem)

    def remove_repair_item(self, index: int) -> RepairItem:
        return removeitem(self, "repair_items", index)

    def clear_repair_items(self) -> Self:
        """Remove all repair items"""
        return clearitems(self, "repair_items")


@item_component_type
class ShooterComponent(ItemComponent):
    """
    Shooter Item Component. Must have the 'minecraft:use_duration' component in order to function properly. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_shooter?view=minecraft-bedrock-stable)
    """

    id = Identifier("shooter")

    def __init__(
        self,
        charge_on_draw: bool,
        max_draw_duration: float,
        scale_power_by_draw_duration: bool,
        ammunition: list[Identifiable] = None,
    ):
        self.ammunition = ammunition
        self.charge_on_draw = charge_on_draw
        self.max_draw_duration = max_draw_duration
        self.scale_power_by_draw_duration = scale_power_by_draw_duration

    def jsonify(self) -> dict:
        data = {
            "ammunition": [str(x) for x in self.ammunition],
            "charge_on_draw": self.charge_on_draw,
            "max_draw_duration": self.max_draw_duration,
            "scale_power_by_draw_duration": self.scale_power_by_draw_duration,
        }
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return ShooterComponent(**data)

    @property
    def ammunition(self) -> list[Identifier]:
        """Ammunition., defaults to None"""
        return getattr2(self, "_ammunition", [])

    @ammunition.setter
    def ammunition(self, value: list[Identifiable]):
        if value is None:
            self.ammunition = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        v = [Identifiable.of(x) for x in value]
        self.on_update("ammunition", v)
        setattr(self, "_ammunition", v)

    @property
    def charge_on_draw(self) -> bool:
        """Charge on draw? Default is set to false."""
        return getattr(self, "_charge_on_draw")

    @charge_on_draw.setter
    def charge_on_draw(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("charge_on_draw", value)
        setattr(self, "_charge_on_draw", value)

    @property
    def max_draw_duration(self) -> float:
        """Draw Duration. Default is set to 0."""
        return getattr(self, "_max_draw_duration")

    @max_draw_duration.setter
    def max_draw_duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("max_draw_duration", v)
        setattr(self, "_max_draw_duration", v)

    @property
    def scale_power_by_draw_duration(self) -> bool:
        """Scale power by draw duration? Default is set to false."""
        return getattr(self, "_scale_power_by_draw_duration")

    @scale_power_by_draw_duration.setter
    def scale_power_by_draw_duration(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("scale_power_by_draw_duration", value)
        setattr(self, "_scale_power_by_draw_duration", value)

    def add_ammunition(self, identifier: Identifiable) -> Identifier:
        self.ammunition.append(Identifiable.of(identifier))
        return identifier

    def remove_ammunition(self, index: int) -> Identifier:
        return self.ammunition.pop(index)

    def clear_ammunitions(self) -> Self:
        self.ammunition = []
        return self


@item_component_type
class ShouldDespawnComponent(SimpleItemComponent):
    """
    Should despawn component determines if the item should eventually despawn while floating in the world [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_should_despawn?view=minecraft-bedrock-stable)
    """

    id = Identifier("should_despawn")
    clazz = bool

    def jsonify(self) -> dict:
        data = {"value": self.value}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return ShouldDespawnComponent(**data)


@item_component_type
class StackedByDataComponent(SimpleItemComponent):
    """
    The stacked by data component determines if the same item with different aux values can stack. Also defines whether the item actors can merge while floating in the world. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_stacked_by_data?view=minecraft-bedrock-stable)
    """

    id = Identifier("stacked_by_data")
    clazz = bool

    @staticmethod
    def from_dict(data: bool) -> Self:
        return StackedByDataComponent(data)


@item_component_type
class ItemTagsComponent(ItemComponent):
    """
    The tags component determines which tags an item has on it. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_tags?view=minecraft-bedrock-stable)
    """

    id = Identifier("tags")

    def __init__(self, tags: list[Identifiable] = None):
        self.tags = tags

    def jsonify(self) -> dict:
        data = {"tags": []}
        for x in self.tags:
            data["tags"].append(str(x))
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return ItemTagsComponent(**data)

    @property
    def tags(self) -> list[Identifier]:
        """An array that can contain multiple item tags., defaults to None"""
        return getattr(self, "_tags", [])

    @tags.setter
    def tags(self, value: list[Identifiable]):
        if value is None:
            self.tags = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        v = [Identifiable.of(x) for x in value]
        self.on_update("tags", v)
        setattr(self, "_tags", v)

    def get_tag(self, index: int) -> Identifier:
        return getitem(self, "tags", index)

    def add_tag(self, tag: Identifiable) -> Identifier:
        return additem(self, "tags", Identifiable.of(tag))

    def remove_tag(self, index: int) -> Identifier:
        return removeitem(self, "tags", index)

    def clear_tags(self) -> Self:
        return clearitems(self, "tags")


@item_component_type
class ThrowableComponent(ItemComponent):
    """
    Throwable item component. Throwable items, such as a snowball. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_throwable?view=minecraft-bedrock-stable)
    """

    id = Identifier("throwable")

    def __init__(
        self,
        do_swing_animation: bool,
        launch_power_scale: int,
        max_draw_duration: float,
        max_launch_power: float,
        min_draw_duration: float,
        scale_power_by_draw_duration: bool,
    ):
        self.do_swing_animation = do_swing_animation
        self.launch_power_scale = launch_power_scale
        self.max_draw_duration = max_draw_duration
        self.max_launch_power = max_launch_power
        self.min_draw_duration = min_draw_duration
        self.scale_power_by_draw_duration = scale_power_by_draw_duration

    def jsonify(self) -> dict:
        data = {
            "do_swing_animation": self.do_swing_animation,
            "launch_power_scale": self.launch_power_scale,
            "max_draw_duration": self.max_draw_duration,
            "max_launch_power": self.max_launch_power,
            "min_draw_duration": self.min_draw_duration,
            "scale_power_by_draw_duration": self.scale_power_by_draw_duration,
        }
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return ThrowableComponent(**data)

    @property
    def do_swing_animation(self) -> bool:
        """Whether the item should use the swing animation when thrown. Default is set to false."""
        return getattr(self, "_do_swing_animation")

    @do_swing_animation.setter
    def do_swing_animation(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("do_swing_animation", value)
        setattr(self, "_do_swing_animation", value)

    @property
    def launch_power_scale(self) -> int:
        """The scale at which the power of the throw increases. Default is set to 1.0."""
        return getattr(self, "_launch_power_scale")

    @launch_power_scale.setter
    def launch_power_scale(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("launch_power_scale", value)
        setattr(self, "_launch_power_scale", value)

    @property
    def max_draw_duration(self) -> float:
        """The maximum duration to draw a throwable item. Default is set to 0.0."""
        return getattr(self, "_max_draw_duration")

    @max_draw_duration.setter
    def max_draw_duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("max_draw_duration", v)
        setattr(self, "_max_draw_duration", v)

    @property
    def max_launch_power(self) -> float:
        """The maximum power to launch the throwable item. Default is set to 1.0."""
        return getattr(self, "_max_launch_power")

    @max_launch_power.setter
    def max_launch_power(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("max_launch_power", v)
        setattr(self, "_max_launch_power", v)

    @property
    def min_draw_duration(self) -> float:
        """The minimum duration to draw a throwable item. Default is set to 0.0."""
        return getattr(self, "_min_draw_duration")

    @min_draw_duration.setter
    def min_draw_duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("min_draw_duration", v)
        setattr(self, "_min_draw_duration", v)

    @property
    def scale_power_by_draw_duration(self) -> bool:
        """Whether or not the power of the throw increases with duration charged. Default is set to false."""
        return getattr(self, "_scale_power_by_draw_duration")

    @scale_power_by_draw_duration.setter
    def scale_power_by_draw_duration(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("scale_power_by_draw_duration", value)
        setattr(self, "_scale_power_by_draw_duration", value)


@item_component_type
class UseAnimationComponent(SimpleItemComponent):
    """
    This component determines which animation plays when using the item. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_use_animation?view=minecraft-bedrock-stable)
    """

    id = Identifier("use_animation")
    clazz = UseAnimation

    def jsonify(self) -> str:
        return self.value.jsonify()

    @staticmethod
    def from_dict(data: UseAnimation | str) -> Self:
        if isinstance(data, str):
            data = UseAnimation.from_dict(data)
        return UseAnimationComponent(data)


@item_component_type
class UseModifiersComponent(ItemComponent):
    """
    This component modifies use effects, including how long the item takes to use and the player's speed when used in combination with components like Shooter, Throwable or Food. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_use_modifiers?view=minecraft-bedrock-stable)
    """

    id = Identifier("use_modifiers")

    def __init__(self, movement_modifier: float, use_duration: float):
        self.movement_modifier = movement_modifier
        self.use_duration = use_duration

    def jsonify(self) -> dict:
        data = {
            "movement_modifier": self.movement_modifier,
            "use_duration": self.use_duration,
        }
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return UseModifiersComponent(**data)

    @property
    def movement_modifier(self) -> float:
        """Modifier value to scale the players movement speed when item is in use."""
        return getattr(self, "_movement_modifier")

    @movement_modifier.setter
    def movement_modifier(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("movement_modifier", v)
        setattr(self, "_movement_modifier", v)

    @property
    def use_duration(self) -> float:
        """How long the item takes to use in seconds."""
        return getattr(self, "_use_duration")

    @use_duration.setter
    def use_duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("use_duration", v)
        setattr(self, "_use_duration", v)


@item_component_type
class WearableComponent(ItemComponent):
    """
    Wearable item component. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_wearable?view=minecraft-bedrock-stable)
    """

    id = Identifier("wearable")

    def __init__(self, protection: int, slot: int):
        self.protection = protection
        self.slot = slot

    def jsonify(self) -> dict:
        data = {"protection": self.protection, "slot": self.slot}
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return WearableComponent(**data)

    @property
    def protection(self) -> int:
        """How much protection the wearable item has. Default is set to 0."""
        return getattr(self, "_protection")

    @protection.setter
    def protection(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("protection", value)
        setattr(self, "_protection", value)

    @property
    def slot(self) -> int:
        """Determines where the item can be worn. If any non-hand slot is chosen, the max stack size is set to 1."""
        return getattr(self, "_slot")

    @slot.setter
    def slot(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("slot", value)
        setattr(self, "_slot", value)


@item_component_type
class DiggerComponent(ItemComponent):
    """
    Digger item component. You can specify how quickly this item can dig specific blocks.
    """

    id = Identifier("digger")

    def __init__(self, use_efficiency: bool, destroy_speeds: list = []):
        self.destroy_speeds = destroy_speeds
        self.use_efficiency = use_efficiency

    def jsonify(self) -> dict:
        data = {
            "destroy_speeds": self.destroy_speeds,
            "use_efficiency": self.use_efficiency,
        }
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return DiggerComponent(**data)

    @property
    def destroy_speeds(self) -> list:
        """A list of blocks to dig with correlating speeds of digging., defaults to None"""
        return getattr2(self, "_destroy_speeds", [])

    @destroy_speeds.setter
    def destroy_speeds(self, value: list):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("destroy_speeds", value)
        setattr(self, "_destroy_speeds", value)

    @property
    def use_efficiency(self) -> bool:
        """Whether this item should be impacted if the efficiency enchant is applied to it."""
        return getattr(self, "_use_efficiency")

    @use_efficiency.setter
    def use_efficiency(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("use_efficiency", value)
        setattr(self, "_use_efficiency", value)


# 1.10


@item_component_type
class UseDurationComponent(SimpleItemComponent):
    """desc"""

    id = Identifier("use_duration")
    clazz = int

    @staticmethod
    def from_dict(data: int) -> Self:
        return UseDurationComponent(data)


@item_component_type
class BlockComponent2(SimpleItemComponent):
    """desc"""

    id = Identifier("block")
    clazz = Identifiable

    def jsonify(self) -> dict:
        return str(self.value)

    @staticmethod
    def from_dict(data: Identifiable) -> Self:
        return BlockComponent2(Identifiable.of(data))


@item_component_type
class CameraComponent(ItemComponent):
    """desc"""

    id = Identifier("camera")

    def __init__(
        self,
        black_bars_duration: float,
        black_bars_screen_ratio: float,
        shutter_duration: float,
        picture_duration: float,
        slide_away_duration: float,
        shutter_screen_ratio: float = 0.0,
    ):
        self.black_bars_duration = black_bars_duration
        self.black_bars_screen_ratio = black_bars_screen_ratio
        self.shutter_duration = shutter_duration
        self.shutter_screen_ratio = shutter_screen_ratio
        self.picture_duration = picture_duration
        self.slide_away_duration = slide_away_duration

    def jsonify(self) -> dict:
        data = {
            "black_bars_duration": self.black_bars_duration,
            "black_bars_screen_ratio": self.black_bars_screen_ratio,
            "shutter_duration": self.shutter_duration,
            "picture_duration": self.picture_duration,
            "slide_away_duration": self.slide_away_duration,
        }
        if self.shutter_screen_ratio:
            data["shutter_screen_ratio"] = self.shutter_screen_ratio
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        return CameraComponent(**data)

    @property
    def black_bars_duration(self) -> float:
        return getattr(self, "_black_bars_duration")

    @black_bars_duration.setter
    def black_bars_duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("black_bars_duration", v)
        setattr(self, "_black_bars_duration", v)

    @property
    def black_bars_screen_ratio(self) -> float:
        return getattr(self, "_black_bars_screen_ratio")

    @black_bars_screen_ratio.setter
    def black_bars_screen_ratio(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("black_bars_screen_ratio", v)
        setattr(self, "_black_bars_screen_ratio", v)

    @property
    def shutter_duration(self) -> float:
        return getattr(self, "_shutter_duration")

    @shutter_duration.setter
    def shutter_duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("shutter_duration", v)
        setattr(self, "_shutter_duration", v)

    @property
    def shutter_screen_ratio(self) -> float:
        return getattr(self, "_shutter_screen_ratio")

    @shutter_screen_ratio.setter
    def shutter_screen_ratio(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("shutter_screen_ratio", v)
        setattr(self, "_shutter_screen_ratio", v)

    @property
    def picture_duration(self) -> float:
        return getattr(self, "_picture_duration")

    @picture_duration.setter
    def picture_duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("picture_duration", v)
        setattr(self, "_picture_duration", v)

    @property
    def slide_away_duration(self) -> float:
        return getattr(self, "_slide_away_duration")

    @slide_away_duration.setter
    def slide_away_duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("slide_away_duration", v)
        setattr(self, "_slide_away_duration", v)


@item_component_type
class PortfolioComponent(EmptyItemComponent):
    """desc"""

    id = Identifier("portfolio")


@item_component_type
class FoilComponent(EmptyItemComponent):
    """desc"""

    id = Identifier("foil")
    clazz = bool


@item_component_type
class SeedComponent(ItemComponent):
    """desc"""

    id = Identifier("seed")

    def __init__(
        self,
        crop_result: Identifiable,
        plant_at_any_solid_surface: bool = None,
        plant_at_face: bool = None,
        plant_at: list[Identifiable] = [],
    ):
        self.crop_result = crop_result
        self.plant_at = plant_at
        self.plant_at_any_solid_surface = plant_at_any_solid_surface
        self.plant_at_face = plant_at_face

    def jsonify(self) -> dict:
        data = {"crop_result": str(self.crop_result)}
        if self.plant_at_any_solid_surface is not None:
            data["plant_at_any_solid_surface"] = self.plant_at_any_solid_surface
        if self.plant_at_face is not None:
            data["plant_at_face"] = self.plant_at_face
        if len(self.plant_at) >= 1:
            data["plant_at"] = [str(x) for x in self.plant_at]
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        if "plant_at" in data:
            if isinstance(data["plant_at"], str):
                data["plant_at"] = [data["plant_at"]]
        return SeedComponent(**data)

    @property
    def plant_at_face(self) -> str:
        return getattr(self, "_plant_at_face", None)

    @plant_at_face.setter
    def plant_at_face(self, value: str):
        if not isinstance(value, str) and value is not None:
            raise TypeError(
                f"Expected str but got '{value.__class__.__name__}' instead"
            )
        self.on_update("plant_at_face", value)
        setattr(self, "_plant_at_face", value)

    @property
    def plant_at_any_solid_surface(self) -> bool:
        return getattr(self, "_plant_at_any_solid_surface", None)

    @plant_at_any_solid_surface.setter
    def plant_at_any_solid_surface(self, value: bool):
        if not isinstance(value, bool) and value is not None:
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("plant_at_any_solid_surface", value)
        setattr(self, "_plant_at_any_solid_surface", value)

    @property
    def crop_result(self) -> Identifier:
        return getattr(self, "_crop_result")

    @crop_result.setter
    def crop_result(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("crop_result", id)
        setattr(self, "_crop_result", id)

    @property
    def plant_at(self) -> list[Identifier]:
        return getattr2(self, "_plant_at", [])

    @plant_at.setter
    def plant_at(self, value: list[Identifiable]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        v = [Identifiable.of(x) for x in value]
        self.on_update("plant_at", v)
        setattr(self, "_plant_at", v)


@item_component_type
class MaxDamageComponent(SimpleItemComponent):
    """desc"""

    id = Identifier("max_damage")
    clazz = int

    @staticmethod
    def from_dict(data: int) -> Self:
        return MaxDamageComponent(data)


@dataclass
class ItemSettings:
    """
    Configure common settings for items
    """

    max_count: int = None
    max_damage: int = None
    recipe_remainder: Identifiable = None
    color: str = None

    def set_count(self, max_count: int) -> Self:
        self.max_count = max_count
        return self

    def set_damage(self, max_damage: int) -> Self:
        self.max_damage = max_damage
        return self

    def set_recipe_remainder(self, recipe_remainder) -> Self:
        self.recipe_remainder = recipe_remainder
        return self

    def rarity(self, color: str) -> Self:
        self.color = color
        return self

    def build(self, item):
        if self.max_count is not None:
            item.add_component(MaxStackSizeComponent(self.max_count))

        if self.max_damage is not None:
            item.add_component(MaxDamageComponent(self.max_damage))

        if self.recipe_remainder is not None:
            item.recipe_remainder = self.recipe_remainder

        if self.color is not None:
            item.add_component(HoverTextColorComponent(self.color))
        return item


@resource_pack
@behavior_pack
class Item(JsonFile, Identifiable):
    """
    Represents a data-driven Item. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemdefinition?view=minecraft-bedrock-stable)
    """

    id = Identifier("item")
    FILEPATH = "items/item.json"

    def __init__(
        self,
        identifier: Identifiable,
        menu_category: MenuCategory = None,
        components: dict[Identifiable, ItemComponent] = None,
        events: dict[Identifiable, Event] = None,
    ):
        Identifiable.__init__(self, identifier)
        self.menu_category = menu_category
        self.components = components
        self.events = events

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "Item{" + str(self.identifier) + "}"

    def jsonify(self) -> dict:
        item = {"description": {"identifier": str(self.identifier)}}
        if self.menu_category:
            item["description"]["menu_category"] = self.menu_category.jsonify()

        if self.components:
            item["components"] = {}
            for k, v in self.components.items():
                item["components"][str(k)] = v.jsonify()

        if self.events:
            item["events"] = {}
            for key, events in self.events.items():
                d = {}
                for k, v in events.items():
                    d[k.path] = v.jsonify()
                item["events"][str(key)] = d

        data = {"format_version": VERSION["ITEM"], str(self.id): item}
        return data

    @property
    def menu_category(self) -> MenuCategory:
        """The creative group name and category for this item, defaults to None"""
        return getattr(self, "_menu_category", None)

    @menu_category.setter
    def menu_category(self, value: MenuCategory):
        if value is None:
            setattr(self, "_menu_category", None)
            return
        if not isinstance(value, MenuCategory):
            raise TypeError(
                f"Expected MenuCategory but got '{value.__class__.__name__}' instead"
            )
        self.on_update("menu_category", value)
        setattr(self, "_menu_category", value)

    @property
    def components(self) -> dict[str, ItemComponent]:
        """List of all components that used in this item, defaults to None"""
        return getattr2(self, "_components", {})

    @components.setter
    def components(self, value: dict[str, ItemComponent]):
        if value is None:
            self.components = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        self.on_update("components", value)
        setattr(self, "_components", value)

    @property
    def events(self) -> dict[Identifier, Event]:
        """List of all events that used in this item, defaults to None"""
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
    def recipe_remainder(self) -> Identifier:
        return getattr(self, "_recipe_remainder", None)

    @recipe_remainder.setter
    def recipe_remainder(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("recipe_remainder", id)
        setattr(self, "_recipe_remainder", id)

    @property
    def name(self) -> str | None:
        return getattr(self, "_name", None)

    @name.setter
    def name(self, value: str):
        setattr(self, "_name", str(value))

    # Read-Only

    @property
    def max_count(self) -> int:
        v = self.get_component("max_stack_size")
        return 64 if v is None else v

    @property
    def max_damage(self) -> int:
        return self.get_component("max_damage")

    @staticmethod
    def from_dict(data: dict) -> Self:
        loader = ItemLoader()
        loader.validate(data)
        return loader.load(data)

    @classmethod
    def from_settings(cls, identifier: Identifiable, settings: ItemSettings):
        if not isinstance(settings, ItemSettings):
            raise TypeError(
                f"Expected ItemSettings but got '{settings.__class__.__name__}' instead"
            )
        self = cls.__new__(cls)
        self.identifier = identifier
        return settings.build(self)

    def translation_key(self) -> str:
        return f"item.{self.identifier}"

    def stack(self):
        return ItemStack(self.identifier)

    def display_name(self, text: str) -> Self:
        """
        The name of this item in-game.

        :rtype: Self
        """
        self.name = text
        return self

    def generate(self, ctx) -> None:
        """
        Called when this item is added to ResourcePack or BehaviorPack

        :type ctx: ResourcePack | BehaviorPack
        """
        for c in self.components.values():
            c.generate(ctx)
        for e in self.events.values():
            for ee in e.values():
                ee.generate(ctx)
        if isinstance(ctx, ResourcePack) and self.name is not None:
            ctx.texts[self.translation_key()] = self.name

    # COMPONENT

    def add_component(self, component: ItemComponent) -> ItemComponent:
        component.generate(self)
        return additem(self, "components", component, component.id, ItemComponent)

    def get_component(self, id: Identifiable) -> ItemComponent:
        return getitem(self, "components", Identifiable.of(id))

    def remove_component(self, id: Identifiable) -> ItemComponent:
        return removeitem(self, "components", Identifiable.of(id))

    def clear_components(self) -> Self:
        """Remove all components"""
        return clearitems(self, "components")

    # EVENT

    def add_event(self, id: Identifiable, event: Event) -> Event:
        if not isinstance(event, Event):
            raise TypeError(
                f"Expected ItemEvent but got '{event.__class__.__name__}' instead"
            )
        i = Identifiable.of(id)
        if i in self.events:
            event.generate(self)
            self.events[i][event.id] = event
            return event
        obj = {}
        obj[event.id] = event
        self.events[i] = obj
        event.id
        return event

    def get_event(self, event: Identifiable) -> Event:
        return getitem(self, "events", Identifiable.of(event))

    def remove_event(self, event: Identifiable) -> Event:
        return removeitem(self, "events", Identifiable.of(event))

    def clear_events(self) -> Self:
        """Remove all events"""
        return clearitems(self, "events")


class BlockItem(Item):
    def __init__(
        self, identifier: Identifiable, block: Identifiable, icon: str, *args, **kw
    ):
        Item.__init__(self, identifier, *args, **kw)
        self.add_component(BlockPlacerComponent(block))
        self.add_component(IconComponent(icon))


class ItemLoader(Loader):
    name = "Item"

    def __init__(self):
        from .schemas import ItemSchema1, ItemSchema2

        Loader.__init__(self, Item)
        self.add_schema(ItemSchema2, "1.10")
        self.add_schema(ItemSchema2, "1.14")
        self.add_schema(ItemSchema2, "1.16")
        self.add_schema(ItemSchema2, "1.16.0")
        self.add_schema(ItemSchema1, "1.20.50")


# UTIL


class ItemStack(Misc):
    def __init__(self, item: Identifiable, count: int = 1, data: int = None):
        self.item = item
        self.count = count
        self.data = data

    def jsonify(self) -> dict:
        data = {"item": str(self.item)}
        if self.count is not None:
            data["count"] = self.count
        if self.data not in [1, None]:
            data["data"] = self.data
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        if isinstance(data, str):
            return ItemStack(data)
        else:
            return ItemStack(**data)

    @property
    def item(self) -> Identifier:
        return getattr(self, "_item")

    @item.setter
    def item(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("item", id)
        setattr(self, "_item", id)

    @property
    def count(self) -> int:
        return getattr(self, "_count", 1)

    @count.setter
    def count(self, value: int):
        if value is None:
            self.count = 1
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("count", value)
        setattr(self, "_count", value)

    @property
    def data(self) -> int:
        return getattr(self, "_data", None)

    @data.setter
    def data(self, value: int):
        if value is None:
            setattr(self, "_data", None)
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("data", value)
        setattr(self, "_data", value)
