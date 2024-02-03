from typing import Self
from dataclasses import dataclass
import json

from . import VERSION
from .registry import INSTANCE, Registries
from .constant import UseAnimation
from .file import JsonFile, Loader
from .util import getattr2, Identifier, MenuCategory, Identifiable
from .event import Event


# COMPONENTS


class ItemComponent:
    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return "ItemComponent{" + str(self.id) + "}"

    @property
    def __dict__(self) -> dict:
        raise NotImplementedError()

    def json(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        raise NotImplementedError()


class SimpleItemComponent(ItemComponent):
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
        if not isinstance(self.clazz, tuple) and issubclass(self.clazz, Identifier):
            if isinstance(value, (Identifier, str)):
                setattr(self, "_value", Identifier(value))
            else:
                raise TypeError(
                    f"Expected {self.clazz.__name__} but got '{value.__class__.__name__}' instead"
                )
        else:
            if isinstance(value, self.clazz):
                setattr(self, "_value", value)
            else:
                raise TypeError(
                    f"Expected {self.clazz.__name__} but got '{value.__class__.__name__}' instead"
                )


class EmptyItemComponent(ItemComponent):
    @property
    def __dict__(self):
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
    id = Identifier("ignores_permission")
    clazz = bool


@item_component_type
class AllowOffHandComponent(SimpleItemComponent):
    """The allow off hand component determines whether the item can be placed in the off hand slot of the inventory."""

    id = Identifier("allow_off_hand")
    clazz = bool


@item_component_type
class BlockPlacerComponent(ItemComponent):
    """Block Placer item component. Items with this component will place a block when used."""

    id = Identifier("block_placer")

    def __init__(self, block: Identifier | str, use_on: list = None):
        self.block = Identifier.parse(block)
        self.use_on = use_on

    @property
    def __dict__(self) -> dict:
        data = {"block": str(self.block)}
        if self.use_on:
            data["use_on"] = self.use_on
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.block = data.pop("block")
        if "use_on" in data:
            self.use_on = data.pop("use_on")
        return self

    @property
    def block(self) -> Identifier:
        """Defines the block that will be placed."""
        return getattr(self, "_block")

    @block.setter
    def block(self, value: Identifier):
        if not isinstance(value, (Identifier, str)):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_block", Identifier(value))

    @property
    def use_on(self) -> list:
        """List of block descriptors that contain blocks that this item can be used on. If left empty, all blocks will be allowed."""
        return getattr2(self, "_use_on", [])

    @use_on.setter
    def use_on(self, value: list):
        if value is None:
            self.use_on = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_use_on", value)


@item_component_type
class CanDestroyInCreativeComponent(SimpleItemComponent):
    """The can destroy in creative component determines if the item will break blocks in creative when swinging."""

    id = Identifier("can_destroy_in_creative")
    clazz = bool


@item_component_type
class CooldownComponent(ItemComponent):
    """Cool down time for a component. After you use an item, all items specified with the same `cool down category` setting becomes unusable for the duration specified by the 'cool down time' setting in this component."""

    id = Identifier("cooldown")

    def __init__(self, category: str, duration: float):
        self.category = category
        self.duration = duration

    @property
    def __dict__(self) -> dict:
        data = {"category": self.category, "duration": self.duration}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.category = data.pop("category")
        self.duration = data.pop("duration")
        return self

    @property
    def category(self) -> str:
        """The type of cool down for this item. All items with a cool down component with the same category are put on cool down when one is used."""
        return getattr(self, "_category")

    @category.setter
    def category(self, value: str):
        setattr(self, "_category", str(value))

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
        setattr(self, "_duration", float(value))


@item_component_type
class DamageComponent(ItemComponent):
    """
    The damage component determines how much extra damage the item does on attack.
    """

    id = Identifier("damage")
    clazz = int

    def __init__(self, value: int):
        self.value = value

    @property
    def __dict__(self) -> dict:
        data = {"value": self.value}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.value = data.pop("value")
        return self


@item_component_type
class ItemDisplayNameComponent(ItemComponent):
    """
    Display Name item component. Determines the text shown whenever an item's name is displayed (ex. hover text).
    """

    id = Identifier("display_name")

    def __init__(self, value: str):
        self.value = value

    @property
    def __dict__(self) -> dict:
        data = {"value": self.value}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.value = data.pop("value")
        return self

    @property
    def value(self) -> str:
        return getattr(self, "_value")

    @value.setter
    def value(self, value: str):
        setattr(self, "_value", str(value))


@item_component_type
class DurabilityComponent(ItemComponent):
    """
    Durability item component. Determines how much damage this item takes before breaking and allows the item to be combined in crafting.
    """

    id = Identifier("durability")

    def __init__(self, damage_chance: float, max_durability: int):
        self.damage_chance = damage_chance
        self.max_durability = max_durability

    @property
    def __dict__(self) -> dict:
        data = {
            "damage_chance": self.damage_chance,
            "max_durability": self.max_durability,
        }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.damage_chance = data.pop("damage_chance")
        self.max_durability = data.pop("max_durability")
        return self

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
        setattr(self, "_damage_chance", float(value))

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
        setattr(self, "_max_durability", value)


@item_component_type
class EnchantableComponent(ItemComponent):
    """
    The enchantable component determines what enchantments can be applied to the item. Not all enchantments will have an effect on all item components.
    """

    id = Identifier("enchantable")

    def __init__(self, slot: str, value: int):
        self.slot = slot
        self.value = value

    @property
    def __dict__(self) -> dict:
        data = {"slot": self.slot, "value": self.value}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.slot = data.pop("slot")
        self.value = data.pop("value")
        return self

    @property
    def slot(self) -> str:
        """What enchantments can be applied (ex. Using `bow` would allow this item to be enchanted as if it were a bow)."""
        return getattr(self, "_slot")

    @slot.setter
    def slot(self, value: str):
        setattr(self, "_slot", str(value))

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
        setattr(self, "_value", value)


@item_component_type
class EntityPlacerComponent(ItemComponent):
    """
    Entity placer item component. You can specifiy allowed blocks that the item is restricted to.
    """

    id = Identifier("entity_placer")

    def __init__(
        self, entity: Identifier | str, dispense_on: list = None, use_on: list = None
    ):
        self.entity = Identifier.parse(entity)
        self.dispense_on = dispense_on
        self.use_on = use_on

    @property
    def __dict__(self) -> dict:
        data = {"entity": str(self.entity)}
        if self.dispense_on:
            data["dispense_on"] = self.dispense_on
        if self.use_on:
            data["use_on"] = self.use_on
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.entity = data.pop("entity")
        if "dispense_on" in data:
            self.dispense_on = data.pop("dispense_on")
        if "use_on" in data:
            self.use_on = data.pop("use_on")
        return self

    @property
    def entity(self) -> Identifier:
        """The entity to be placed in the world."""
        return getattr(self, "_entity")

    @entity.setter
    def entity(self, value: Identifier):
        if not isinstance(value, (Identifier, str)):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_entity", Identifier(value))

    @property
    def dispense_on(self) -> list:
        """List of block descriptors that contain blocks that this item can be dispensed on. If left empty, all blocks will be allowed., defaults to None"""
        return getattr2(self, "_dispense_on", [])

    @dispense_on.setter
    def dispense_on(self, value: list):
        if value is None:
            self.dispense_on = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_dispense_on", value)

    @property
    def use_on(self) -> list:
        """List of block descriptors that contain blocks that this item can be used on. If left empty, all blocks will be allowed., defaults to None"""
        return getattr2(self, "_use_on", [])

    @use_on.setter
    def use_on(self, value: list):
        if value is None:
            self.use_on = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_use_on", value)


@item_component_type
class FoodComponent(ItemComponent):
    """
    When an item has a food component, it becomes edible to the player. Must have the 'minecraft:use_duration' component in order to function properly.
    """

    id = Identifier("food")

    def __init__(
        self,
        nutrition: int,
        saturation_modifier: float = None,
        can_always_eat: bool = False,
        using_converts_to: Identifier | str = None,
    ):
        self.nutrition = nutrition
        self.saturation_modifier = saturation_modifier
        self.can_always_eat = can_always_eat
        self.using_converts_to = using_converts_to

    @property
    def __dict__(self) -> dict:
        data = {}
        if self.nutrition is not None:
            data["nutrition"] = self.nutrition
        if self.saturation_modifier not in [None, 0.6]:
            data["saturation_modifier"] = self.saturation_modifier
        if self.can_always_eat is not False:
            data["can_always_eat"] = self.can_always_eat
        if self.using_converts_to is not None:
            data["using_converts_to"] = str(self.using_converts_to)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "nutrition" in data:
            self.nutrition = data.pop("nutrition")
        if "saturation_modifier" in data:
            self.saturation_modifier = data.pop("saturation_modifier")
        if "can_always_eat" in data:
            self.can_always_eat = data.pop("can_always_eat")
        if "using_converts_to" in data:
            self.using_converts_to = data.pop("using_converts_to")
        return self

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
        setattr(self, "_saturation_modifier", float(value))

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
        setattr(self, "_can_always_eat", value)

    @property
    def using_converts_to(self) -> Identifier | None:
        """When used, converts to the item specified by the string in this field. Default does not convert item., defaults to None"""
        return getattr(self, "_using_converts_to", None)

    @using_converts_to.setter
    def using_converts_to(self, value: Identifier | None):
        if value is None:
            setattr(self, "_using_converts_to", None)
        else:
            setattr(self, "_using_converts_to", Identifier(value))


@item_component_type
class FuelComponent(ItemComponent):
    """
    Fuel item component. Allows this item to be used as fuel in a furnace to 'cook' other items.
    """

    id = Identifier("fuel")

    def __init__(self, duration: float):
        self.duration = duration

    @property
    def __dict__(self) -> dict:
        data = {"duration": self.duration}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.duration = data.pop("duration")
        return self

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
        setattr(self, "_duration", float(value))


@item_component_type
class GlintComponent(SimpleItemComponent):
    """
    The glint component determines whether the item has the enchanted glint render effect on it.
    """

    id = Identifier("glint")
    clazz = bool

    @property
    def __dict__(self) -> dict:
        data = {"value": self.value}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.value = data.pop("value")
        return self


@item_component_type
class HandEquippedComponent(SimpleItemComponent):
    """
    This component determines if an item is rendered like a tool while in hand.
    """

    id = Identifier("hand_equipped")
    clazz = bool


@item_component_type
class HoverTextColorComponent(SimpleItemComponent):
    """
    The hover text color component determines the color of the item name when hovering over it.
    """

    id = Identifier("hover_text_color")
    clazz = str

    @property
    def __dict__(self) -> dict:
        data = {"value": self.value}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.value = data.pop("value")
        return self


@item_component_type
class IconComponent(ItemComponent):
    """
    Icon item component. Determines the icon to represent the item in the UI and elsewhere.
    """

    id = Identifier("icon")

    def __init__(self, texture: Identifier | str):
        self.texture = texture

    @property
    def __dict__(self) -> dict:
        data = {"texture": str(self.texture)}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.texture = data.pop("texture")
        return self

    @property
    def texture(self) -> Identifier:
        """The key from the resource_pack/textures/item_texture.json 'texture_data' object associated with the texture file."""
        return getattr(self, "_texture")

    @texture.setter
    def texture(self, value: Identifier | str):
        setattr(self, "_texture", Identifier(value))


@item_component_type
class InteractButtonComponent(SimpleItemComponent):
    """
    This component is a boolean or string that determines if the interact button is shown in touch controls and what text is displayed on the button. When set as true, default "Use Item" text will be used.z
    """

    id = Identifier("interact_button")
    clazz = (str, bool)

    @property
    def __dict__(self) -> dict:
        data = {"value": self.value}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.value = data.pop("value")
        return self


@item_component_type
class ItemStorageComponent(ItemComponent):
    """
    The Storage Item Component is used for storing Items within an Item's User Data
    """

    id = Identifier("item_storage")

    def __init__(self, capacity: int):
        self.capacity = capacity

    @property
    def __dict__(self) -> dict:
        data = {"capacity": self.capacity}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.capacity = data.pop("capacity")
        return self

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
        setattr(self, "_capacity", value)


@item_component_type
class LiquidClippedComponent(SimpleItemComponent):
    """
    The liquid clipped component determines whether the item interacts with liquid blocks on use.
    """

    id = Identifier("liquid_clipped")
    clazz = bool

    @property
    def __dict__(self) -> dict:
        data = {"value": self.value}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.value = data.pop("value")
        return self


@item_component_type
class MaxStackSizeComponent(SimpleItemComponent):
    """
    The max stack size component determines how many of the item can be stacked together.
    """

    id = Identifier("max_stack_size")
    clazz = int


@item_component_type
class ProjectileComponent(ItemComponent):
    """
    Projectile item component. projectile items shoot out, like an arrow.
    """

    id = Identifier("projectile")

    def __init__(
        self, projectile_entity: Identifier | str, minimum_critical_power: float
    ):
        self.projectile_entity = Identifier.parse(projectile_entity)
        self.minimum_critical_power = minimum_critical_power

    @property
    def __dict__(self) -> dict:
        data = {
            "projectile_entity": str(self.projectile_entity),
            "minimum_critical_power": self.minimum_critical_power,
        }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.projectile_entity = data.pop("projectile_entity")
        self.minimum_critical_power = data.pop("minimum_critical_power")
        return self

    @property
    def projectile_entity(self) -> Identifier:
        """How long you must charge a projectile for it to critically hit."""
        return getattr(self, "_projectile_entity")

    @projectile_entity.setter
    def projectile_entity(self, value: Identifier):
        if not isinstance(value, (Identifier, str)):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_projectile_entity", Identifier(value))

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
        setattr(self, "_minimum_critical_power", float(value))


@item_component_type
class RecordComponent(ItemComponent):
    """
    Record Item Component. Used by record items to play music.
    """

    id = Identifier("record")

    def __init__(
        self, comparator_signal: int, duration: float, sound_event: Identifier | str
    ):
        self.comparator_signal = comparator_signal
        self.duration = duration
        self.sound_event = Identifier.parse(sound_event)

    @property
    def __dict__(self) -> dict:
        data = {
            "comparator": self.comparator_signal,
            "duration": self.duration,
            "sound_event": str(self.sound_event),
        }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.comparator_signal = data.pop("comparator")
        self.duration = data.pop("duration")
        self.sound_event = data.pop("sound_event")
        return self

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
        setattr(self, "_duration", float(value))

    @property
    def sound_event(self) -> Identifier:
        """Sound event type: 13, cat, blocks, chirp, far, mall, mellohi, stal, strad, ward, 11, wait, pigstep, otherside, 5, relic."""
        return getattr(self, "_sound_event")

    @sound_event.setter
    def sound_event(self, value: Identifier):
        if not isinstance(value, (Identifier, str)):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_sound_event", Identifier(value))


class RepairItem:
    pass


@item_component_type
class RepairableComponent(ItemComponent):
    """
    Repairable item component. Determines the items that can be used to repair this item along with how much durability they repair.
    """

    id = Identifier("repairable")

    def __init__(self, repair_items: list[RepairItem] = None):
        self.repair_items = repair_items

    @property
    def __dict__(self) -> dict:
        data = {"repair_items": []}
        for i in self.repair_items:
            data["repair_items"].append(i.__dict__)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.repair_items = data.pop("repair_items")
        return self

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
        setattr(self, "_repair_items", value)


@item_component_type
class ShooterComponent(ItemComponent):
    """
    Shooter Item Component. Must have the 'minecraft:use_duration' component in order to function properly.
    """

    id = Identifier("shooter")

    def __init__(
        self,
        charge_on_draw: bool,
        max_draw_duration: float,
        scale_power_by_draw_duration: bool,
        ammunition: list[Identifier] = None,
    ):
        self.ammunition = ammunition
        self.charge_on_draw = charge_on_draw
        self.max_draw_duration = max_draw_duration
        self.scale_power_by_draw_duration = scale_power_by_draw_duration

    @property
    def __dict__(self) -> dict:
        data = {
            "ammunition": [str(x) for x in self.ammunition],
            "charge_on_draw": self.charge_on_draw,
            "max_draw_duration": self.max_draw_duration,
            "scale_power_by_draw_duration": self.scale_power_by_draw_duration,
        }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.ammunition = data.pop("ammunition")
        self.charge_on_draw = data.pop("charge_on_draw")
        self.max_draw_duration = data.pop("max_draw_duration")
        self.scale_power_by_draw_duration = data.pop("scale_power_by_draw_duration")
        return self

    @property
    def ammunition(self) -> list[Identifier]:
        """Ammunition., defaults to None"""
        return getattr2(self, "_ammunition", [])

    @ammunition.setter
    def ammunition(self, value: list[Identifier]):
        if value is None:
            self.ammunition = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_ammunition", value)

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
        setattr(self, "_max_draw_duration", float(value))

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
        setattr(self, "_scale_power_by_draw_duration", value)

    def add_ammunition(self, identifier: Identifier) -> Identifier:
        if not isinstance(identifier, (Identifier, str)):
            raise TypeError(
                f"Expected Identifier but got '{identifier.__class__.__name__}' instead"
            )
        self.ammunition.append(Identifier(identifier))
        return identifier

    def remove_ammunition(self, index: int) -> Identifier:
        return self.ammunition.pop(index)

    def clear_ammunitions(self) -> Self:
        self.ammunition = []
        return self


@item_component_type
class ShouldDespawnComponent(SimpleItemComponent):
    """
    Should despawn component determines if the item should eventually despawn while floating in the world
    """

    id = Identifier("should_despawn")
    clazz = bool

    @property
    def __dict__(self) -> dict:
        data = {"value": self.value}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.value = data.pop("value")
        return self


@item_component_type
class StackedByDataComponent(SimpleItemComponent):
    """
    The stacked by data component determines if the same item with different aux values can stack. Also defines whether the item actors can merge while floating in the world.
    """

    id = Identifier("stacked_by_data")
    clazz = bool


@item_component_type
class TagsComponent(ItemComponent):
    """
    The tags component determines which tags an item has on it.
    """

    id = Identifier("tags")

    def __init__(self, tags: list[Identifier | str] = None):
        self.tags = tags

    @property
    def __dict__(self) -> dict:
        data = {"tags": []}
        for x in self.tags:
            data["tags"].append(str(x))
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.tags = data.pop("tags")
        return self

    @property
    def tags(self) -> list[Identifier | str]:
        """An array that can contain multiple item tags., defaults to None"""
        return getattr(self, "_tags", [])

    @tags.setter
    def tags(self, value: list[Identifier | str]):
        if value is None:
            self.tags = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_tags", value)


@item_component_type
class ThrowableComponent(ItemComponent):
    """
    Throwable item component. Throwable items, such as a snowball.
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

    @property
    def __dict__(self) -> dict:
        data = {
            "do_swing_animation": self.do_swing_animation,
            "launch_power_scale": self.launch_power_scale,
            "max_draw_duration": self.max_draw_duration,
            "max_launch_power": self.max_launch_power,
            "min_draw_duration": self.min_draw_duration,
            "scale_power_by_draw_duration": self.scale_power_by_draw_duration,
        }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.do_swing_animation = data.pop("do_swing_animation")
        self.launch_power_scale = data.pop("launch_power_scale")
        self.max_draw_duration = data.pop("max_draw_duration")
        self.max_launch_power = data.pop("max_launch_power")
        self.min_draw_duration = data.pop("min_draw_duration")
        self.scale_power_by_draw_duration = data.pop("scale_power_by_draw_duration")
        return self

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
        setattr(self, "_max_draw_duration", float(value))

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
        setattr(self, "_max_launch_power", float(value))

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
        setattr(self, "_min_draw_duration", float(value))

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
        setattr(self, "_scale_power_by_draw_duration", value)


@item_component_type
class UseAnimationComponent(SimpleItemComponent):
    """
    This component determines which animation plays when using the item.
    """

    id = Identifier("use_animation")
    clazz = UseAnimation

    @property
    def __dict__(self) -> str:
        return self.value._value_

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.value = UseAnimation[data]
        return self


@item_component_type
class UseModifiersComponent(ItemComponent):
    """
    This component modifies use effects, including how long the item takes to use and the player's speed when used in combination with components like Shooter, Throwable or Food.
    """

    id = Identifier("use_modifiers")

    def __init__(self, movement_modifier: float, use_duration: float):
        self.movement_modifier = movement_modifier
        self.use_duration = use_duration

    @property
    def __dict__(self) -> dict:
        data = {
            "movement_modifier": self.movement_modifier,
            "use_duration": self.use_duration,
        }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.movement_modifier = data.pop("movement_modifier")
        self.use_duration = data.pop("use_duration")
        return self

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
        setattr(self, "_movement_modifier", float(value))

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
        setattr(self, "_use_duration", float(value))


@item_component_type
class WearableComponent(ItemComponent):
    """
    Wearable item component.
    """

    id = Identifier("wearable")

    def __init__(self, protection: int, slot: int):
        self.protection = protection
        self.slot = slot

    @property
    def __dict__(self) -> dict:
        data = {"protection": self.protection, "slot": self.slot}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.protection = data.pop("protection")
        self.slot = data.pop("slot")
        return self

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
        setattr(self, "_slot", value)


@item_component_type
class DiggerComponent(ItemComponent):
    """
    Digger item component. You can specify how quickly this item can dig specific blocks.
    """

    id = Identifier("digger")

    def __init__(self, use_efficiency: bool, destroy_speeds: list = None):
        self.destroy_speeds = destroy_speeds
        self.use_efficiency = use_efficiency

    @property
    def __dict__(self) -> dict:
        data = {
            "destroy_speeds": self.destroy_speeds,
            "use_efficiency": self.use_efficiency,
        }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.destroy_speeds = data.pop("destroy_speeds")
        self.use_efficiency = data.pop("use_efficiency")
        return self

    @property
    def destroy_speeds(self) -> list:
        """A list of blocks to dig with correlating speeds of digging., defaults to None"""
        return getattr2(self, "_destroy_speeds", [])

    @destroy_speeds.setter
    def destroy_speeds(self, value: list):
        if value is None:
            self.destroy_speeds = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
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
        setattr(self, "_use_efficiency", value)


# 1.10


@item_component_type
class UseDurationComponent(SimpleItemComponent):
    id = Identifier("use_duration")
    clazz = int


@item_component_type
class BlockComponent2(SimpleItemComponent):
    id = Identifier("block")
    clazz = Identifier


@item_component_type
class CameraComponent(ItemComponent):
    id = Identifier("camera")

    def __init__(
        self,
        black_bars_duration: float,
        black_bars_screen_ratio: float,
        shutter_duration: float,
        shutter_screen_ratio: float,
        picture_duration: float,
        slide_away_duration: float,
    ):
        self.black_bars_duration = black_bars_duration
        self.black_bars_screen_ratio = black_bars_screen_ratio
        self.shutter_duration = shutter_duration
        self.shutter_screen_ratio = shutter_screen_ratio
        self.picture_duration = picture_duration
        self.slide_away_duration = slide_away_duration

    @property
    def __dict__(self) -> dict:
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

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.black_bars_duration = data.pop("black_bars_duration")
        self.black_bars_screen_ratio = data.pop("black_bars_screen_ratio")
        self.shutter_duration = data.pop("shutter_duration")
        self.picture_duration = data.pop("picture_duration")
        self.slide_away_duration = data.pop("slide_away_duration")
        if "shutter_screen_ratio" in data:
            self.shutter_screen_ratio = data.pop("shutter_screen_ratio")
        return self

    @property
    def black_bars_duration(self) -> float:
        return getattr(self, "_black_bars_duration")

    @black_bars_duration.setter
    def black_bars_duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_black_bars_duration", float(value))

    @property
    def black_bars_screen_ratio(self) -> float:
        return getattr(self, "_black_bars_screen_ratio")

    @black_bars_screen_ratio.setter
    def black_bars_screen_ratio(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_black_bars_screen_ratio", float(value))

    @property
    def shutter_duration(self) -> float:
        return getattr(self, "_shutter_duration")

    @shutter_duration.setter
    def shutter_duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_shutter_duration", float(value))

    @property
    def shutter_screen_ratio(self) -> float:
        return getattr(self, "_shutter_screen_ratio")

    @shutter_screen_ratio.setter
    def shutter_screen_ratio(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_shutter_screen_ratio", float(value))

    @property
    def picture_duration(self) -> float:
        return getattr(self, "_picture_duration")

    @picture_duration.setter
    def picture_duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_picture_duration", float(value))

    @property
    def slide_away_duration(self) -> float:
        return getattr(self, "_slide_away_duration")

    @slide_away_duration.setter
    def slide_away_duration(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_slide_away_duration", float(value))


@item_component_type
class PortfolioComponent(EmptyItemComponent):
    id = Identifier("portfolio")


@item_component_type
class FoilComponent(EmptyItemComponent):
    id = Identifier("foil")
    clazz = bool


@item_component_type
class SeedComponent(ItemComponent):
    id = Identifier("seed")

    def __init__(self, crop_result: Identifier):
        self.crop_result = crop_result

    @property
    def __dict__(self) -> dict:
        data = {"crop_result": self.crop_result}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.crop_result = data.pop("crop_result")
        return self

    @property
    def crop_result(self) -> Identifier:
        return getattr(self, "_crop_result")

    @crop_result.setter
    def crop_result(self, value: Identifier):
        if not isinstance(value, (Identifier, str)):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_crop_result", Identifier(value))


@item_component_type
class MaxDamageComponent(SimpleItemComponent):
    id = Identifier("max_damage")
    clazz = int


@dataclass
class ItemSettings:
    """
    Configure common settings for items
    """

    max_count: int = None
    max_damage: int = None
    recipe_remainder: Identifier = None
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


class Item(JsonFile, Identifiable):
    """
    Represents an Item.
    """

    id = Identifier("item")
    EXTENSION: str = ".json"
    FILENAME: str = "item"
    DIRNAME: str = "items"

    def __init__(
        self,
        identifier: Identifier,
        menu_category: MenuCategory = None,
        components: dict[Identifier, ItemComponent] = None,
        events: dict[Identifier, Event] = None,
    ):
        Identifiable.__init__(self, identifier)
        self.menu_category = menu_category
        self.components = components
        self.events = events

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "Item{" + str(self.identifier) + "}"

    @property
    def __dict__(self) -> dict:
        item = {"description": {"identifier": str(self.identifier)}}
        if self.menu_category:
            item["description"]["menu_category"] = self.menu_category.__dict__

        if self.components:
            item["components"] = {}
            for k, v in self.components.items():
                item["components"][str(k)] = v.__dict__

        if self.events:
            item["events"] = {}
            for key, events in self.events.items():
                d = {}
                for k, v in events.items():
                    d[k.path] = v.__dict__
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
        setattr(self, "_components", value)

    @property
    def events(self) -> dict[Identifier, Event]:
        """List of all events that used in this item, defaults to None"""
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
    def recipe_remainder(self) -> Identifier:
        return getattr(self, "_recipe_remainder")

    @recipe_remainder.setter
    def recipe_remainder(self, value: Identifier):
        if not isinstance(value, Identifier):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_recipe_remainder", value)

    # Read-Only

    @property
    def max_count(self) -> int:
        v = self.get_component("max_stack_size")
        return 64 if v is None else v

    @property
    def max_damage(self) -> int:
        return self.get_component("max_damage")

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = ItemLoader()
        loader.validate(data)
        return loader.load(data)

    @classmethod
    def from_settings(cls, identifier: Identifier, settings: ItemSettings):
        if not isinstance(settings, ItemSettings):
            raise TypeError(
                f"Expected ItemSettings but got '{settings.__class__.__name__}' instead"
            )
        self = cls.__new__(cls)
        self.identifier = identifier

        if settings.max_count is not None:
            self.add_component(MaxStackSizeComponent(settings.max_count))

        if settings.max_damage is not None:
            self.add_component(MaxDamageComponent(settings.max_damage))

        if settings.recipe_remainder is not None:
            self.recipe_remainder = settings.recipe_remainder

        if settings.color is not None:
            self.add_component(HoverTextColorComponent(settings.color))

        return self

    def translation_key(self) -> str:
        return "item." + str(self.id)

    def stack(self):
        return ItemStack(self.identifier)

    # COMPONENT

    def add_component(self, component: ItemComponent) -> ItemComponent:
        if not isinstance(component, ItemComponent):
            raise TypeError(
                f"Expected ItemComponent but got '{component.__class__.__name__}' instead"
            )
        self.components[component.id] = component
        return component

    def get_component(self, id: str) -> ItemComponent:
        x = id.id if isinstance(id, ItemComponent) else id
        return self.components.get(x)

    def remove_component(self, id: str) -> ItemComponent:
        x = id.id if isinstance(id, ItemComponent) else id
        return self.components.pop(x)

    def clear_components(self) -> Self:
        self.components.clear()
        return self

    # EVENT

    def add_event(self, id: Identifier | str, event: Event) -> Event:
        if not isinstance(event, Event):
            raise TypeError(
                f"Expected ItemEvent but got '{event.__class__.__name__}' instead"
            )
        i = Identifier.parse(id)
        if i in self.events:
            self.events[i][event.id] = event
            return event
        obj = {}
        obj[event.id] = event
        self.events[i] = obj
        event.id
        return event

    def get_event(self, id: Identifier | str) -> Event:
        i = Identifier.parse(id)
        return self.events.get(i)

    def remove_event(self, id: Identifier | str) -> Event:
        i = Identifier.parse(id)
        return self.events.pop(i)

    def clear_events(self) -> Self:
        self.events.clear()
        return self


class ItemLoader(Loader):
    name = "Item"

    def __init__(self):
        from .schemas import ItemSchema1, ItemSchema2

        Loader.__init__(self, Item)
        self.add_schema(ItemSchema2, "1.10")
        self.add_schema(ItemSchema2, "1.14")
        self.add_schema(ItemSchema2, "1.16")
        self.add_schema(ItemSchema2, "1.16.0")
        self.add_schema(ItemSchema1, "1.20.51")


# UTIL


class ItemStack:
    def __init__(self, item: Identifier | Item, count: int = 1, data: int = None):
        self.item = item
        self.count = count
        self.data = data

    @property
    def __dict__(self) -> dict:
        data = {"item": str(self.item)}
        if self.count is not None:
            data["count"] = self.count
        if self.data not in [1, None]:
            data["data"] = self.data
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if isinstance(data, str):
            self.item = data
        else:
            self.item = data.pop("item")
            if "count" in data:
                self.count = data.pop("count")
            if "data" in data:
                self.data = data.pop("data")
        return self

    @property
    def item(self) -> Identifier:
        return getattr(self, "_item")

    @item.setter
    def item(self, value: Identifier):
        if isinstance(value, Item):
            self.item = value.identifier
        else:
            setattr(self, "_item", Identifier(value))

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
        setattr(self, "_data", value)
