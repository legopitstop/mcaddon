from typing import Self
import os

from .pack import behavior_pack
from .exception import TypeNotFoundError
from .constant import Destination
from .registry import INSTANCE, Registries
from .file import JsonFile
from .util import (
    getattr2,
    getitem,
    removeitem,
    clearitems,
    additem,
    Identifier,
    Identifiable,
    Misc,
)
from .block import Block
from .item import Item

# TODO: Needs get, add, remove, and clear methods


class LootNumberProvider(Misc):
    def __init__(self, min: float, max: float = None):
        """
        :param min: the minimum value
        :type min: float
        :param max: the maximum value, defaults to None
        :type max: float, optional
        """
        self.min = min
        self.max = max

    def jsonify(self) -> dict:
        data = {}
        if self.min:
            data["min"] = self.min
        if self.max:
            data["max"] = self.max
        if self.min is not None and self.max is None:
            data = self.min
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if isinstance(data, dict):
            self.min = data.pop("min")
            self.max = data.pop("max")
        else:
            self.min = data
        return self

    @property
    def min(self) -> float:
        return getattr(self, "_min")

    @min.setter
    def min(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("min", v)
        setattr(self, "_min", v)

    @property
    def max(self) -> float:
        return getattr(self, "_max", None)

    @max.setter
    def max(self, value: float):
        if value is None:
            setattr(self, "_max", None)
            return
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("max", v)
        setattr(self, "_max", v)


class Enchant(Misc):
    def __init__(self, id: Identifiable, levels: LootNumberProvider):
        """
        An enchantment

        :param id: an enchantment ID
        :type id: Identifiable
        :param levels: the level of the enchantment
        :type levels: LootNumberProvider
        """
        self.id = id
        self.levels = levels

    def jsonify(self) -> dict:
        data = {"id": str(self.id)}
        if self.levels:
            data["levels"] = {
                "range_min": self.levels.min,
                "range_max": self.levels.max,
            }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "id" in data:
            self.id = data.pop("id")
        if "levels" in data:
            self.levels = LootNumberProvider.from_dict(data.pop("levels"))
        return self

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("id", id)
        setattr(self, "_id", id)

    @property
    def levels(self) -> LootNumberProvider:
        return getattr(self, "_levels", None)

    @levels.setter
    def levels(self, value: LootNumberProvider):
        if not isinstance(value, LootNumberProvider):
            raise TypeError(
                f"Expected LootNumberProvider but got '{value.__class__.__name__}' instead"
            )
        self.on_update("levels", value)
        setattr(self, "_levels", value)


# CONDITIONS
#  https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable


class LootCondition(Misc):
    def __call__(self, ctx) -> int:
        return self.execute(ctx)

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier.of(value))

    def execute(self, ctx) -> int:
        return 0

    def jsonify(self) -> dict:
        data = {"condition": str(self.id)}
        return data


INSTANCE.create_registry(Registries.LOOT_CONDITION_TYPE, LootCondition)


def loot_condition(cls):
    """
    Add this loot condition to the registry
    """

    def wrapper():
        if not issubclass(cls, LootCondition):
            raise TypeError(f"Expected LootCondition but got '{cls.__name__}' instead")
        return INSTANCE.register(Registries.LOOT_CONDITION_TYPE, cls.id, cls)

    return wrapper()


@loot_condition
class HasMarkVariantLootCondition(LootCondition):
    id = Identifier("has_mark_variant")

    def __init__(self, value: int):
        """
        Specifies that there are different variations for the loot
        """
        self.value = value

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["value"] = self.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.value = data.pop("value")
        return self

    @property
    def value(self) -> int:
        return getattr(self, "_value")

    @value.setter
    def value(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("value", value)
        setattr(self, "_value", value)


@loot_condition
class HasVariantLootCondition(LootCondition):
    id = Identifier("has_variant")

    def __init__(self, value: int):
        """
        Specifies that there are different variations for the loot
        """
        self.value = value

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["value"] = self.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.value = data.pop("value")
        return self

    @property
    def value(self) -> int:
        return getattr(self, "_value")

    @value.setter
    def value(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("value", value)
        setattr(self, "_value", value)


@loot_condition
class KilledByPlayerOrPetsLootCondition(LootCondition):
    id = Identifier("killed_by_player_or_pets")

    def __init__(self):
        """
        Can supply another way to customize a loot drop, depending on how the entity was killed
        """
        pass

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        return self


@loot_condition
class RandomChanceLootCondition(LootCondition):
    id = Identifier("random_chance")

    def __init__(self, chance: float):
        """
        Condition that applies a given value to the chances that loot will drop
        """
        self.chance = chance

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["chance"] = self.chance
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.chance = data.pop("chance")
        return self

    @property
    def chance(self) -> float:
        return getattr(self, "_chance")

    @chance.setter
    def chance(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("chance", v)
        setattr(self, "_chance", v)


@loot_condition
class RandomChanceWithLootingLootCondition(LootCondition):
    id = Identifier("random_chance_with_looting")

    def __init__(self, chance: float, looting_multiplier: float):
        """
        Similar to the random_chance condition, but also includes a multiplier value
        """
        self.chance = chance
        self.looting_multiplier = looting_multiplier

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["chance"] = self.chance
        data["looting_multiplier"] = self.looting_multiplier
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.chance = data.pop("chance")
        self.looting_multiplier = data.pop("looting_multiplier")
        return self

    @property
    def chance(self) -> float:
        return getattr(self, "_chance")

    @chance.setter
    def chance(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("chance", v)
        setattr(self, "_chance", v)

    @property
    def looting_multiplier(self) -> float:
        return getattr(self, "_looting_multiplier")

    @looting_multiplier.setter
    def looting_multiplier(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("looting_multiplier", v)
        setattr(self, "_looting_multiplier", v)


@loot_condition
class RandomDifficultyChanceLootCondition(LootCondition):
    id = Identifier("random_difficulty_chance")

    def __init__(self, default_chance: float, peaceful: float, hard: float):
        """
        Condition that can control loot drops depending on the difficulty level
        """
        self.default_chance = default_chance
        self.peaceful = peaceful
        self.hard = hard

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["default_chance"] = self.default_chance
        if self.peaceful:
            data["peaceful"] = self.peaceful
        if self.hard:
            data["hard"] = self.hard
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.default_chance = data.pop("default_chance")
        if "peaceful" in data:
            self.peaceful = data.pop("peaceful")
        if "hard" in data:
            self.hard = data.pop("hard")
        return self

    @property
    def default_chance(self) -> float:
        return getattr(self, "_default_chance")

    @default_chance.setter
    def default_chance(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("default_chance", v)
        setattr(self, "_default_chance", v)

    @property
    def peaceful(self) -> float:
        return getattr(self, "_peaceful", None)

    @peaceful.setter
    def peaceful(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("peaceful", v)
        setattr(self, "_peaceful", v)

    @property
    def hard(self) -> float:
        return getattr(self, "_hard", None)

    @hard.setter
    def hard(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("hard", v)
        setattr(self, "_hard", v)


@loot_condition
class RandomRegionalDifficultyChanceLootCondition(LootCondition):
    id = Identifier("random_regional_difficulty_chance")

    def __init__(self, max_chance: float):
        """
        Determines loot probability according to the region.
        """
        self.max_chance = max_chance

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["max_chance"] = self.max_chance
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.max_chance = data.pop("max_chance")
        return self

    @property
    def max_chance(self) -> float:
        return getattr(self, "_max_chance")

    @max_chance.setter
    def max_chance(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("max_chance", v)
        setattr(self, "_max_chance", v)


@loot_condition
class MatchToolLootCondition(LootCondition):
    id = Identifier("match_tool")

    def __init__(
        self,
        item: Identifiable,
        count: LootNumberProvider,
        durability: LootNumberProvider,
        enchantments: list[Enchant],
    ):
        """
        Checks whether the tool (or weapon/item the player is using) used to make the loot drop matches the modifier conditions provided. The predicates used are: count, durability, enchantments, and item

        :param item: An item ID
        :type item: Identifiable
        :param count: amount of the item
        :type count: LootNumberProvider
        :param durability: the durability of the item
        :type durability: LootNumberProvider
        :param enchantments: list of enchantments
        :type enchantments: list[Enchant]
        """
        self.item = item
        self.count = count
        self.durability = durability
        self.enchantments = enchantments

    def jsonify(self) -> dict:
        data = super().jsonify()
        if self.item:
            data["item"] = str(self.item)
        if self.count:
            data["count"] = {"range_min": self.count.min, "range_max": self.count.max}
        if self.durability:
            data["durability"] = {
                "range_min": self.durability.min,
                "range_max": self.durability.max,
            }
        if self.enchantments:
            data["enchantments"] = [x.jsonify() for x in self.enchantments]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "item" in data:
            self.item = data.pop("item")
        if "count" in data:
            self.count = LootNumberProvider.from_dict(data.pop("count"))
        if "durability" in data:
            self.durability = LootNumberProvider.from_dict(data.pop("durability"))
        if "enchantments" in data:
            self.enchantments = [Enchant.from_dict(x) for x in data.pop("enchantments")]
        return self

    @property
    def item(self) -> Identifier:
        return getattr(self, "_item")

    @item.setter
    def item(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("item", id)
        setattr(self, "_item", id)

    @property
    def count(self) -> LootNumberProvider:
        return getattr(self, "_count")

    @count.setter
    def count(self, value: LootNumberProvider):
        if not isinstance(value, LootNumberProvider):
            raise TypeError(
                f"Expected LootNumberProvider but got '{value.__class__.__name__}' instead"
            )
        self.on_update("count", value)
        setattr(self, "_count", value)

    @property
    def durability(self) -> LootNumberProvider:
        return getattr(self, "_durability")

    @durability.setter
    def durability(self, value: LootNumberProvider):
        if not isinstance(value, LootNumberProvider):
            raise TypeError(
                f"Expected LootNumberProvider but got '{value.__class__.__name__}' instead"
            )
        self.on_update("durability", value)
        setattr(self, "_durability", value)

    @property
    def enchantments(self) -> list[Enchant]:
        return getattr(self, "_enchantments")

    @enchantments.setter
    def enchantments(self, value: list[Enchant]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("enchantments", value)
        setattr(self, "_enchantments", value)

    def get_enchantment(self, index: int) -> Enchant:
        return getitem(self, "enchantments", index)

    def add_enchantment(self, enchant: Enchant) -> Enchant:
        return additem(self, "enchantments", enchant)

    def remove_enchantment(self, index: int) -> Enchant:
        return removeitem(self, "enchantments", index)

    def clear_enchantments(self) -> Self:
        """Remove all enchantments"""
        return clearitems(self, "enchantments")


@loot_condition
class KilledByEntityLootCondition(LootCondition):
    id = Identifier("killed_by_entity")

    def __init__(self, entity_type: Identifiable):
        self.entity_type = entity_type

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["entity_type"] = str(self.entity_type)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.entity_type = data.pop("entity_type")
        return self

    @property
    def entity_type(self) -> Identifier:
        return getattr(self, "_entity_type")

    @entity_type.setter
    def entity_type(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("entity_type", id)
        setattr(self, "_entity_type", id)


@loot_condition
class EntityKilledLootCondition(LootCondition):
    id = Identifier("entity_killed")

    def __init__(self, entity_type: Identifiable):
        self.entity_type = entity_type

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["entity_type"] = str(self.entity_type)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.entity_type = data.pop("entity_type")
        return self

    @property
    def entity_type(self) -> Identifier:
        return getattr(self, "_entity_type")

    @entity_type.setter
    def entity_type(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("entity_type", id)
        setattr(self, "_entity_type", id)


@loot_condition
class KilledByPlayerLootCondition(LootCondition):
    id = Identifier("killed_by_player")

    def __init__(self):
        pass

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        return self


# FUNCTIONS
#  https://learn.microsoft.com/en-us/minecraft/creator/documents/lootandtradetablefunctions?view=minecraft-bedrock-stable


class LootFunction(Misc):

    def __call__(self, ctx) -> int:
        return self.execute(ctx)

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier.of(value))

    def jsonify(self) -> dict:
        data = {"function": str(self.id)}
        return data

    def execute(self, ctx) -> int:
        return 0


INSTANCE.create_registry(Registries.LOOT_FUNCTION_TYPE, LootFunction)


def loot_function(cls):
    """
    Add this loot function to the registry
    """

    def wrapper():
        if not issubclass(cls, LootFunction):
            raise TypeError(f"Expected LootFunction but got '{cls.__name__}' instead")
        return INSTANCE.register(Registries.LOOT_FUNCTION_TYPE, cls.id, cls)

    return wrapper()


# trade table only
@loot_function
class EnchantBookForTradingLootFunction(LootFunction):
    id = Identifier("enchant_book_for_trading")

    def __init__(
        self,
        base_cost: int,
        base_random_cost: int,
        per_level_random_cost: int,
        per_level_cost: int,
    ):
        """
        This function enchants a book using the algorithm for enchanting items sold by villagers
        """
        self.base_cost = base_cost
        self.base_random_cost = base_random_cost
        self.per_level_random_cost = per_level_random_cost
        self.per_level_cost = per_level_cost

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["base_cost"] = self.base_cost
        data["base_random_cost"] = self.base_random_cost
        data["per_level_random_cost"] = self.per_level_random_cost
        data["per_level_cost"] = self.per_level_cost
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.base_cost = data.pop("base_cost")
        self.base_random_cost = data.pop("base_random_cost")
        self.per_level_random_cost = data.pop("per_level_random_cost")
        self.per_level_cost = data.pop("per_level_cost")
        return self

    @property
    def base_cost(self) -> int:
        return getattr(self, "_base_cost")

    @base_cost.setter
    def base_cost(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("base_cost", value)
        setattr(self, "_base_cost", value)

    @property
    def base_random_cost(self) -> int:
        return getattr(self, "_base_random_cost")

    @base_random_cost.setter
    def base_random_cost(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("base_random_cost", value)
        setattr(self, "_base_random_cost", value)

    @property
    def per_level_random_cost(self) -> int:
        return getattr(self, "_per_level_random_cost")

    @per_level_random_cost.setter
    def per_level_random_cost(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("per_level_random_cost", value)
        setattr(self, "_per_level_random_cost", value)

    @property
    def per_level_cost(self) -> int:
        return getattr(self, "_per_level_cost")

    @per_level_cost.setter
    def per_level_cost(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("per_level_cost", value)
        setattr(self, "_per_level_cost", value)


class StewEffect:
    def __init__(self, id: int):
        self.id = id

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.id = data["id"]
        return self

    def jsonify(self) -> dict:
        data = {"id": self.id}
        return data


@loot_function
class SetStewEffectLootFunction(LootFunction):
    id = Identifier("set_stew_effect")

    def __init__(self, effects: list[StewEffect]):
        """
        This function sets stew effects on a suspicious_stew item.
        """
        self.effects = effects

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["effects"] = [x.jsonify() for x in self.effects]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.effects = [StewEffect.from_dict(x) for x in data.pop("effects")]
        return self

    @property
    def effects(self) -> list[StewEffect]:
        return getattr(self, "_effects")

    @effects.setter
    def effects(self, value: list[StewEffect]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("effects", value)
        setattr(self, "_effects", value)

    def get_effect(self, index: int) -> StewEffect:
        return getitem(self, "effects", index)

    def add_effect(self, effect: StewEffect) -> StewEffect:
        return additem(self, "effects", effect, type=StewEffect)

    def remove_effect(self, index: int) -> StewEffect:
        return removeitem(self, "effects", index)

    def clear_effects(self) -> Self:
        return clearitems(self, "effects")


@loot_function
class EnchantRandomGearLootFunction(LootFunction):
    id = Identifier("enchant_random_gear")

    def __init__(self, chance: float):
        """
        Enchants an item utilizing the same algorithm used while enchanting equipment vanilla mobs spawn with. Takes a chance modifier to manipulate the algorithm. Note that a chance modifier of 1.0 doesn't mean a 100% chance that gear will become enchanted. Rather, the chance is modified based on the difficulty. On Peaceful and Easy difficulties, the chance will always be 0% no matter what. On Hard difficulty, a chance of 1.0 will be 100%, but the chance is roughly 2/3 that on Normal difficulty
        """
        self.chance = chance

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["chance"] = self.chance
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.chance = data.pop("chance")
        return self

    @property
    def chance(self) -> float:
        return getattr(self, "_chance")

    @chance.setter
    def chance(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("chance", v)
        setattr(self, "_chance", v)


@loot_function
class EnchantRandomlyLootFunction(LootFunction):
    id = Identifier("enchant_randomly")

    def __init__(self, treasure: bool):
        """
        Generates a random enchantment that is compatible with the item. Supports the optional treasure boolean (true/false) to allow treasure enchantments to be toggled on and off. Treasure enchantments are enchantments that cannot be obtained through the enchanting table, including Frost Walker, Mending, Soul Speed, Curse of Binding, and Curse of Vanishing
        """
        self.treasure = treasure

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["treasure"] = self.treasure
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "treasure" in data:
            self.treasure = data.pop("treasure")
        return self

    @property
    def treasure(self) -> bool:
        return getattr(self, "_treasure", False)

    @treasure.setter
    def treasure(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("treasure", value)
        setattr(self, "_treasure", value)


@loot_function
class EnchantWithLevelsLootFunction(LootFunction):
    id = Identifier("enchant_with_levels")

    def __init__(self, treasure: bool, levels: LootNumberProvider):
        """
        Applies an enchantment as if it were enchanted through an enchanting table using a minimum and maximum XP level defined through the levels parameter. The treasure boolean (true/false) will allow treasure-only enchantments to be used. Treasure enchantments are enchantments that cannot be obtained through the enchanting table, including Frost Walker, Mending, Soul Speed, Curse of Binding, and Curse of Vanishing.
        """
        self.treasure = treasure
        self.levels = levels

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["treasure"] = self.treasure
        data["levels"] = self.levels.jsonify()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.treasure = data.pop("treasure")
        self.levels = LootNumberProvider.from_dict(data.pop("levels"))
        return self

    @property
    def treasure(self) -> bool:
        return getattr(self, "_treasure")

    @treasure.setter
    def treasure(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("treasure", value)
        setattr(self, "_treasure", value)

    @property
    def levels(self) -> LootNumberProvider:
        return getattr(self, "_levels")

    @levels.setter
    def levels(self, value: LootNumberProvider):
        if not isinstance(value, LootNumberProvider):
            raise TypeError(
                f"Expected LootNumberProvider but got '{value.__class__.__name__}' instead"
            )
        self.on_update("levels", value)
        setattr(self, "_levels", value)


@loot_function
class SpecificEnchantsLootFunction(LootFunction):
    id = Identifier("specific_enchants")

    def __init__(self, enchants: list[Enchant] = []):
        """
        This function allows you to set a list of specific enchantments on an item. It also allows you to apply enchantments to items that wouldn't normally be enchantable in-game.
        """
        self.enchants = enchants

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["enchants"] = [x.jsonify() for x in self.enchants]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.enchants = [Enchant.from_dict(x) for x in data.pop("enchants")]
        return self

    @property
    def enchantments(self) -> list[Enchant]:
        return getattr(self, "_enchantments")

    @enchantments.setter
    def enchantments(self, value: list[Enchant]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("enchantments", value)
        setattr(self, "_enchantments", value)

    def get_enchantment(self, index: int) -> Enchant:
        return getitem(self, "enchantments", index)

    def add_enchantment(self, enchant: Enchant) -> Enchant:
        return additem(self, "enchantments", enchant)

    def remove_enchantment(self, index: int) -> Enchant:
        return removeitem(self, "enchantments", index)

    def clear_enchantments(self) -> Self:
        """Remove all enchantments"""
        return clearitems(self, "enchantments")


# loot table only
@loot_function
class LootingEnchantLootFunction(LootFunction):
    id = Identifier("looting_enchant")

    def __init__(self, count: LootNumberProvider):
        """
        This function allows you to modify the count of how many items are returned when an entity is killed by an item with the looting enchantment. Due to that, it only works with loot tables, and only if that loot table is called by the death of an entity.
        """
        self.count = count

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["count"] = self.count.jsonify()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.count = LootNumberProvider.from_dict(data.pop("count"))
        return self

    @property
    def count(self) -> LootNumberProvider:
        return getattr(self, "_count")

    @count.setter
    def count(self, value: LootNumberProvider):
        if not isinstance(value, LootNumberProvider):
            raise TypeError(
                f"Expected LootNumberProvider but got '{value.__class__.__name__}' instead"
            )
        self.on_update("count", value)
        setattr(self, "_count", value)


@loot_function
class RandomAuxValueLootFunction(LootFunction):
    id = Identifier("random_aux_value")

    def __init__(self, values: LootNumberProvider):
        """
        Similar to random_block_state, this allows you to pick a random auxiliary value for an item. The following example will result in a randomly-colored dye.
        """
        self.values = values

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["values"] = self.values.jsonify()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.values = LootNumberProvider.from_dict(data.pop("values"))
        return self

    @property
    def values(self) -> LootNumberProvider:
        return getattr(self, "_values")

    @values.setter
    def values(self, value: LootNumberProvider):
        if not isinstance(value, LootNumberProvider):
            raise TypeError(
                f"Expected LootNumberProvider but got '{value.__class__.__name__}' instead"
            )
        self.on_update("values", value)
        setattr(self, "_values", value)


@loot_function
class RandomBlockPropertyLootFunction(LootFunction):
    id = Identifier("random_block_state")

    def __init__(self, block_state: Identifiable, values: LootNumberProvider):
        """
        This allows you to randomize the block state of the resulting item. For instance, the following example code can drop stone (0), granite (1), polished granite (2), diorite (3), polished diorite (4), or andesite (5).
        """
        self.block_state = block_state
        self.values = values

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["block_state"] = str(self.block_state)
        data["values"] = self.values.jsonify()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.block_state = data.pop("block_state")
        self.values = LootNumberProvider.from_dict(data.pop("values"))
        return self

    @property
    def block_state(self) -> Identifier:
        return getattr(self, "_block_state")

    @block_state.setter
    def block_state(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("block_state", id)
        setattr(self, "_block_state", id)

    @property
    def values(self) -> LootNumberProvider:
        return getattr(self, "_values")

    @values.setter
    def values(self, value: LootNumberProvider):
        if not isinstance(value, LootNumberProvider):
            raise TypeError(
                f"Expected LootNumberProvider but got '{value.__class__.__name__}' instead"
            )
        self.on_update("values", value)
        setattr(self, "_values", value)


@loot_function
class RandomDyeLootFunction(LootFunction):
    id = Identifier("random_dye")

    def __init__(self):
        """
        This function affects the colors of the random leather items supplied by a leather worker.
        """
        pass

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        return self


@loot_function
class SetActorIdLootFunction(LootFunction):
    id = Identifier("set_actor_id")

    def __init__(self, actor_id: Identifiable):
        """
        This function only works with a spawn egg and is used to set the entity ID of that spawn egg.
        """
        self.actor_id = actor_id

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["id"] = str(self.actor_id)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.actor_id = data.pop("id")
        return self

    @property
    def actor_id(self) -> Identifier:
        return getattr(self, "_actor_id")

    @actor_id.setter
    def actor_id(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("actor_id", id)
        setattr(self, "_actor_id", id)


@loot_function
class SetBannerDetailsLootFunction(LootFunction):
    id = Identifier("set_banner_details")

    def __init__(self, type: int):
        """
        This function only works on banners and currently only supports a banner type of 1. A banner type of 1 results in an illager banner.
        """
        self.type = type

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["type"] = self.type
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.type = data.pop("type")
        return self

    @property
    def type(self) -> int:
        return getattr(self, "_type")

    @type.setter
    def type(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("type", value)
        setattr(self, "_type", value)


@loot_function
class SetBookContentsLootFunction(LootFunction):
    id = Identifier("set_book_contents")

    def __init__(self, author: str, title: str, pages: list[str]):
        """
        This function allows you to set the contents of a book.
        """
        self.author = author
        self.title = title
        self.pages = pages

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["author"] = self.author
        data["title"] = self.title
        data["pages"] = self.pages
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.author = data.pop("author")
        self.title = data.pop("title")
        self.pages = data.pop("pages")
        return self

    @property
    def author(self) -> str:
        return getattr(self, "_author")

    @author.setter
    def author(self, value: str):
        v = str(value)
        self.on_update("author", v)
        setattr(self, "_author", v)

    @property
    def title(self) -> str:
        return getattr(self, "_title")

    @title.setter
    def title(self, value: str):
        v = str(value)
        self.on_update("title", v)
        setattr(self, "_title", v)

    @property
    def pages(self) -> list[str]:
        return getattr(self, "_pages")

    @pages.setter
    def pages(self, value: list[str]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("pages", value)
        setattr(self, "_pages", value)

    def get_page(self, index: int) -> str:
        return getitem(self, "pages", index)

    def add_page(self, page: str):
        return additem(self, "pages", str(page))

    def remove_page(self, index: int) -> str:
        return removeitem(self, "pages", index)

    def clear_pages(self) -> Self:
        """Remove all pages"""
        return clearitems(self, "pages")


@loot_function
class SetCountLootFunction(LootFunction):
    id = Identifier("set_count")

    def __init__(self, count: LootNumberProvider):
        """
        Sets the quantity of items returned by setting the count value
        """
        self.count = count

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["count"] = self.count.jsonify()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.count = LootNumberProvider.from_dict(data.pop("count"))
        return self

    @property
    def count(self) -> LootNumberProvider:
        return getattr(self, "_count")

    @count.setter
    def count(self, value: LootNumberProvider):
        if not isinstance(value, LootNumberProvider):
            raise TypeError(
                f"Expected LootNumberProvider but got '{value.__class__.__name__}' instead"
            )
        self.on_update("count", value)
        setattr(self, "_count", value)


@loot_function
class SetDamageLootFunction(LootFunction):
    id = Identifier("set_damage")

    def __init__(self, damage: LootNumberProvider):
        """
        Sets the percentage of durability remaining for items that have durability by setting the damage value. 1.0 is 100% of durability remaining (undamaged) while 0.0 is no durability remaining.
        """
        self.damage = damage

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["damage"] = self.damage.jsonify()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.damage = LootNumberProvider.from_dict(data.pop("damage"))
        return self

    @property
    def damage(self) -> LootNumberProvider:
        return getattr(self, "_damage")

    @damage.setter
    def damage(self, value: LootNumberProvider):
        if not isinstance(value, LootNumberProvider):
            raise TypeError(
                f"Expected LootNumberProvider but got '{value.__class__.__name__}' instead"
            )
        self.on_update("damage", value)
        setattr(self, "_damage", value)


@loot_function
class SetDataLootFunction(LootFunction):
    id = Identifier("set_data")

    def __init__(self, data: int):
        """
        Sets the data value of a block or item to an exact id. This is useful for things like returning a specific potion or specific color of item. It also allows you to return different block values, like a specific log type
        """
        self.data = data

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["data"] = self.data
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.data = data.pop("data")
        return self

    @property
    def data(self) -> int:
        return getattr(self, "_data")

    @data.setter
    def data(self, value: int):
        if not isinstance(value, (int, dict)):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("data", value)
        setattr(self, "_data", value)


@loot_function
class SetDataFromColorIndexLootFunction(LootFunction):
    id = Identifier("set_data_from_color_index")

    def __init__(self):
        """
        Inherits the data value of the resulting item from the associated entity's color index. An in-game example would be a pink sheep dropping pink wool on death. If the associated entity doesn't have a color index set (or it's used inside a chest's loot table), it will always result in a data value of 0.
        """
        pass

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        return self


@loot_function
class SetLoreLootFunction(LootFunction):
    id = Identifier("set_lore")

    def __init__(self, lore: list[str] = []):
        """
        This function allows you to set the lore of an item. Each line within the lore object represents a single line of text. There's currently no support for rawtext.
        """
        self.lore = lore

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["lore"] = self.lore
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.lore = data.pop("lore")
        return self

    @property
    def lore(self) -> list[str]:
        return getattr(self, "_lore")

    @lore.setter
    def lore(self, value: list[str]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("lore", value)
        setattr(self, "_lore", value)

    def get_lore(self, index: int) -> str:
        return getitem(self, "lore", index)

    def add_lore(self, text: str) -> str:
        return additem(self, "lore", str(text))

    def remove_lore(self, index: int) -> str:
        return removeitem(self, "lore", index)

    def clear_lores(self) -> Self:
        """Remove all lore"""
        return clearitems(self, "lore")


@loot_function
class SetNameLootFunction(LootFunction):
    id = Identifier("set_name")

    def __init__(self, name: str):
        """
        This function allows you to set the name of an item. There's currently no support for rawtext.
        """
        self.name = name

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["name"] = self.name
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.name = data.pop("name")
        return self

    @property
    def name(self) -> str:
        return getattr(self, "_name")

    @name.setter
    def name(self, value: str):
        v = str(value)
        self.on_update("name", v)
        setattr(self, "_name", v)


@loot_function
class ExplorationMapLootFunction(LootFunction):
    id = Identifier("exploration_map")

    def __init__(self, destination: Destination):
        """
        Transforms a normal map into a treasure map that marks the location of hidden treasure. The destination value defines what type of treasure map they receive.
        """
        self.destination = destination

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["destination"] = self.destination.jsonify()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.destination = Destination.from_dict(data.pop("destination"))
        return self

    @property
    def destination(self) -> Destination:
        return getattr(self, "_destination")

    @destination.setter
    def destination(self, value: Destination):
        if not isinstance(value, Destination):
            raise TypeError(
                f"Expected Destination but got '{value.__class__.__name__}' instead"
            )
        self.on_update("destination", value)
        setattr(self, "_destination", value)


@loot_function
class FillContainerLootFunction(LootFunction):
    id = Identifier("fill_container")

    def __init__(self, loot_table: str):
        """
        This function allows you to define the loot table for a chest. When the item is generated and the player places it, it will be full of the contents defined inside the referenced loot table.

        Loot tables for chests are generated at the time of opening or breaking. Consider it a Schrödinger's box. The content of the chest isn't decided until you look inside.
        """
        self.loot_table = loot_table

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["loot_table"] = self.loot_table
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.loot_table = data.pop("loot_table")
        return self

    @property
    def loot_table(self) -> str:
        return getattr(self, "_loot_table")

    @loot_table.setter
    def loot_table(self, value: str):
        v = str(value)
        self.on_update("loot_table", v)
        setattr(self, "_loot_table", v)


# loot table only
@loot_function
class FurnaceSmeltLootFunction(LootFunction):
    id = Identifier("furnace_smelt")

    def __init__(self):
        """
        If the item to return has a smelted crafting recipe and the loot table is triggered by an entity killed with fire (Fire Aspect, flint and steel, lava, etc), the result will be the smelted version of the item. Due to these requirements, this function does not work in villager trades or with chests. This function only works if used in conjunction with the minecraft:loot behavior.
        """
        pass

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        return self


@loot_function
class TraderMaterialTypeLootFunction(LootFunction):
    id = Identifier("trader_material_type")

    def __init__(self):
        """
        This function affects the type of items a fisherman wants to trade for other items, such as a boat.
        """
        pass

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        return self


# ENTRY


class LootPoolEntry(Misc):
    def __init__(self, conditions: list[LootCondition] = []):
        self.conditions = conditions

    def jsonify(self) -> dict:
        data = {"type": str(self.id.path)}
        if self.conditions:
            data["conditions"] = [x.jsonify() for x in self.conditions]
        return data

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier.of(value))

    @property
    def conditions(self) -> list[LootCondition]:
        return getattr2(self, "_conditions", [])

    @conditions.setter
    def conditions(self, value: list[LootCondition]):
        if value is None:
            self.conditions = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("conditions", value)
        setattr(self, "_conditions", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "conditions" in data:
            v = []
            for x in data.pop("conditions"):
                id = x.get("condition")
                clazz = INSTANCE.get_registry(Registries.LOOT_CONDITION_TYPE).get(id)
                if clazz is None:
                    raise TypeNotFoundError(repr(id))
                v.append(clazz.from_dict(x))
            self.conditions = v
        return self

    def get_condition(self, index: int) -> LootCondition:
        return getitem(self, "conditions", index)

    def add_condition(self, condition: LootCondition) -> LootCondition:
        return additem(self, "conditions", condition, type=LootCondition)

    def remove_condition(self, index: int) -> LootCondition:
        return removeitem(self, "conditions", index)

    def clear_conditions(self) -> Self:
        return clearitems(self, "conditions")


INSTANCE.create_registry(Registries.POOL_ENTRY_TYPE, LootPoolEntry)


def pool_entry(cls):
    """
    Add this loot pool entry to the registry
    """

    def wrapper():
        if not issubclass(cls, LootPoolEntry):
            raise TypeError(f"Expected LootPoolEntry but got '{cls.__name__}' instead")
        return INSTANCE.register(Registries.POOL_ENTRY_TYPE, cls.id, cls)

    return wrapper()


class LeafEntry(LootPoolEntry):
    def __init__(
        self,
        weight: int = None,
        quality: int = None,
        conditions: list[LootCondition] = [],
        functions: list[LootFunction] = [],
    ):
        LootPoolEntry.__init__(self, conditions)
        self.weight = weight
        self.quality = quality
        self.functions = functions

    def jsonify(self) -> dict:
        data = super().jsonify()
        if self.weight not in [None, 1]:
            data["weight"] = self.weight
        if self.quality not in [None, 1]:
            data["quality"] = self.quality
        if self.functions:
            data["functions"] = [x.jsonify() for x in self.functions]
        return data

    @property
    def weight(self) -> int:
        return getattr2(self, "_weight", 1)

    @weight.setter
    def weight(self, value: int):
        if value is None:
            self.weight = 1
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("weight", value)
        setattr(self, "_weight", value)

    @property
    def quality(self) -> int:
        return getattr2(self, "_quality", 1)

    @quality.setter
    def quality(self, value: int):
        if value is None:
            self.quality = 1
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("quality", value)
        setattr(self, "_quality", value)

    @property
    def functions(self) -> list[LootFunction]:
        return getattr2(self, "_functions", [])

    @functions.setter
    def functions(self, value: list[LootFunction]):
        if value is None:
            self.functions = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("functions", value)
        setattr(self, "_functions", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        if "weight" in data:
            self.weight = data.pop("weight")
        if "quality" in data:
            self.quality = data.pop("quality")

        if "functions" in data:
            v = []
            for x in data.pop("functions"):
                id = x.get("function")
                clazz = INSTANCE.get_registry(Registries.LOOT_FUNCTION_TYPE).get(id)
                if clazz is None:
                    raise TypeNotFoundError(repr(id))
                v.append(clazz.from_dict(x))
            self.functions = v
        return self

    def get_function(self, index: int) -> LootFunction:
        return getitem(self, "functions", index)

    def add_function(self, function: LootFunction) -> LootFunction:
        return additem(self, "functions", function, type=LootFunction)

    def remove_function(self, index: int) -> LootFunction:
        return removeitem(self, "functions", index)

    def clear_functions(self) -> Self:
        """Remove all functions"""
        return clearitems(self, "functions")


@pool_entry
class ItemEntry(LeafEntry):
    id = Identifier("item")

    def __init__(
        self,
        name: Identifiable,
        weight: int = None,
        quality: int = None,
        conditions: list[LootCondition] = [],
        functions: list[LootFunction] = [],
    ):
        LeafEntry.__init__(self, weight, quality, conditions, functions)
        self.name = name

    def __str__(self) -> str:
        return "ItemEntry{" + str(self.item) + "}"

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["name"] = str(self.name)
        return data

    @property
    def name(self) -> Identifier:
        return getattr(self, "_name")

    @name.setter
    def name(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("name", id)
        setattr(self, "_name", id)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        if "name" in data:
            self.name = data.pop("name")
        return self


@pool_entry
class LootEntry(LeafEntry):
    id = Identifier("loot_table")

    def __init__(
        self,
        name: str,
        weight: int = None,
        quality: int = None,
        conditions: list[LootCondition] = [],
        functions: list[LootFunction] = [],
    ):
        LeafEntry.__init__(self, weight, quality, conditions, functions)
        self.name = name

    def __str__(self) -> str:
        return "LootEntry{" + repr(self.name) + "}"

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["name"] = self.name
        return data

    @property
    def name(self) -> str:
        return getattr(self, "_name")

    @name.setter
    def name(self, value: str):
        v = str(value)
        self.on_update("name", v)
        setattr(self, "_name", v)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        if "name" in data:
            self.name = data.pop("name")
        return self


@pool_entry
class EmptyEntry(LeafEntry):
    id = Identifier("empty")

    def __init__(
        self,
        weight: int = None,
        quality: int = None,
        conditions: list[LootCondition] = [],
        functions: list[LootFunction] = [],
    ):
        LeafEntry.__init__(self, weight, quality, conditions, functions)


# MISC


class LootTiers(Misc):
    def __init__(self, initial_range: int, bonus_rolls: int, bonus_chance: float):
        self.initial_range = initial_range
        self.bonus_rolls = bonus_rolls
        self.bonus_chance = bonus_chance

    def jsonify(self) -> dict:
        data = {"initial_range": self.initial_range}
        if self.bonus_rolls:
            data["bonus_rolls"] = self.bonus_rolls
        if self.bonus_chance:
            data["bonus_chance"] = self.bonus_chance
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.initial_range = data.pop("initial_range")
        if "bonus_rolls" in data:
            self.bonus_rolls = data.pop("bonus_rolls")
        if "bonus_chance" in data:
            self.bonus_chance = data.pop("bonus_chance")
        return self

    @property
    def initial_range(self) -> int:
        return getattr(self, "_initial_range")

    @initial_range.setter
    def initial_range(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("initial_range", value)
        setattr(self, "_initial_range", value)

    @property
    def bonus_rolls(self) -> int:
        return getattr(self, "_bonus_rolls", None)

    @bonus_rolls.setter
    def bonus_rolls(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("bonus_rolls", value)
        setattr(self, "_bonus_rolls", value)

    @property
    def bonus_chance(self) -> float:
        return getattr(self, "_bonus_chance", None)

    @bonus_chance.setter
    def bonus_chance(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        v = float(value)
        self.on_update("bonus_chance", v)
        setattr(self, "_bonus_chance", v)


class LootPool(Misc):
    def __init__(
        self,
        rolls: LootNumberProvider = None,
        bonus_rolls: LootNumberProvider = None,
        tiers: LootTiers = None,
        entries: list[LootPoolEntry] = [],
        conditions: list[LootCondition] = [],
        functions: list[LootFunction] = [],
    ):
        self.rolls = rolls
        self.bonus_rolls = bonus_rolls
        self.tiers = tiers
        self.entries = entries
        self.conditions = conditions
        self.functions = functions

    def __iter__(self):
        for entry in self.entries:
            yield entry

    def __getitem__(self, index: int) -> LootPoolEntry:
        return self.entries[index]

    def jsonify(self) -> dict:
        data = {"entries": [x.jsonify() for x in self.entries]}
        if self.tiers:
            data["tiers"] = self.tiers.jsonify()
        if self.conditions:
            data["conditions"] = [x.jsonify() for x in self.conditions]
        if self.functions:
            data["functions"] = [x.jsonify() for x in self.functions]
        if self.rolls not in [None, 1.0]:
            data["rolls"] = self.rolls.jsonify()
        if self.bonus_rolls not in [None, 1.0]:
            data["bonus_rolls"] = self.bonus_rolls.jsonify()
        return data

    @property
    def tiers(self) -> LootTiers | None:
        return getattr(self, "_tiers", None)

    @tiers.setter
    def tiers(self, value: LootTiers):
        if value is None:
            setattr(self, "_tiers", None)
            return
        if not isinstance(value, LootTiers):
            raise TypeError(
                f"Expected LootTiers but got '{value.__class__.__name__}' instead"
            )
        self.on_update("tiers", value)
        setattr(self, "_tiers", value)

    @property
    def entries(self) -> list[LootPoolEntry]:
        return getattr2(self, "_entries", [])

    @entries.setter
    def entries(self, value: list[LootPoolEntry]):
        if value is None:
            self.entries = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("entries", value)
        setattr(self, "_entries", value)

    @property
    def conditions(self) -> list[LootCondition]:
        return getattr2(self, "_conditions", [])

    @conditions.setter
    def conditions(self, value: list[LootCondition]):
        if value is None:
            self.conditions = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("conditions", value)
        setattr(self, "_conditions", value)

    @property
    def functions(self) -> list[LootFunction]:
        return getattr2(self, "_functions", [])

    @functions.setter
    def functions(self, value: list[LootFunction]):
        if value is None:
            self.functions = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("functions", value)
        setattr(self, "_functions", value)

    @property
    def rolls(self) -> LootNumberProvider:
        return getattr2(self, "_rolls", LootNumberProvider(1))

    @rolls.setter
    def rolls(self, value: LootNumberProvider):
        if value is None:
            self.rolls = LootNumberProvider(1)
            return
        elif isinstance(value, (float, int)):
            self.rolls = LootNumberProvider(float(value))
            return
        if not isinstance(value, LootNumberProvider):
            raise TypeError(
                f"Expected LootNumberProvider but got '{value.__class__.__name__}' instead"
            )
        self.on_update("rolls", value)
        setattr(self, "_rolls", value)

    @property
    def bonus_rolls(self) -> LootNumberProvider:
        return getattr2(self, "_bonus_rolls", LootNumberProvider(0.0))

    @bonus_rolls.setter
    def bonus_rolls(self, value: LootNumberProvider):
        if value is None:
            self.bonus_rolls = LootNumberProvider(0.0)
            return
        if not isinstance(value, LootNumberProvider):
            raise TypeError(
                f"Expected LootNumberProvider but got '{value.__class__.__name__}' instead"
            )
        self.on_update("bonus_rolls", value)
        setattr(self, "_bonus_rolls", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "tiers" in data:
            self.tiers = LootTiers.from_dict(data.pop("tiers"))
        if "entries" in data:
            v = []
            for x in data.pop("entries"):
                id = x.get("type")
                clazz = INSTANCE.get_registry(Registries.POOL_ENTRY_TYPE).get(id)
                if clazz is None:
                    raise TypeNotFoundError(repr(id))
                v.append(clazz.from_dict(x))
            self.entries = v

        if "conditions" in data:
            v = []
            for x in data.pop("conditions"):
                id = x.get("condition")
                clazz = INSTANCE.get_registry(Registries.LOOT_CONDITION_TYPE).get(id)
                if clazz is None:
                    raise TypeNotFoundError(repr(id))
                v.append(clazz.from_dict(x))
            self.conditions = v

        if "functions" in data:
            v = []
            for x in data.pop("functions"):
                id = x.get("function")
                clazz = INSTANCE.get_registry(Registries.LOOT_FUNCTION_TYPE).get(id)
                if clazz is None:
                    raise TypeNotFoundError(repr(id))
                v.append(clazz.from_dict(x))
            self.functions = v

        if "rolls" in data:
            self.rolls = LootNumberProvider.from_dict(data.pop("rolls"))
        if "bonus_rolls" in data:
            self.bonus_rolls = LootNumberProvider.from_dict(data.pop("bonus_rolls"))
        return self

    def get_entry(self, index: int) -> LootPoolEntry:
        return getitem(self, "entries", index)

    def add_entry(self, entry: LootPoolEntry) -> LootPoolEntry:
        return additem(self, "entries", entry, type=LootPoolEntry)

    def remove_entry(self, index: int) -> LootPoolEntry:
        return removeitem(self, "entries", index)

    def clear_entries(self) -> Self:
        """Remove all entries"""
        return clearitems(self, "entries")

    def get_condition(self, index: int) -> LootCondition:
        return getitem(self, "entries", index)

    def add_condition(self, condition: LootCondition) -> LootCondition:
        return additem(self, "conditions", condition, type=LootCondition)

    def remove_condition(self, index: int) -> LootCondition:
        return removeitem(self, "conditions", index)

    def clear_conditions(self) -> Self:
        """Remove all conditions"""
        return clearitems(self, "conditions")

    def get_function(self, index: int) -> LootFunction:
        return getitem(self, "functions", index)

    def add_function(self, function: LootFunction) -> LootFunction:
        return additem(self, "functions", function, type=LootFunction)

    def remove_function(self, index: int) -> LootFunction:
        return removeitem(self, "functions", index)

    def clear_functions(self) -> Self:
        """Remove all functions"""
        return clearitems(self, "functions")


@behavior_pack
class LootTable(JsonFile, Identifiable):
    """
    Represents a Loot Table.
    """

    id = Identifier("loot_table")
    FILEPATH = "loot_tables/loot_table.json"

    def __init__(
        self,
        identifier: Identifiable = None,
        pools: list[LootPool] = None,
        functions: list[LootFunction] = None,
    ):
        Identifiable.__init__(self, identifier)
        self.pools = pools
        self.functions = functions

    def __str__(self) -> str:
        return "LootTable{" + repr(self.identifier.path) + "}"

    def __iter__(self):
        for pool in self.pools:
            yield pool

    def __getitem__(self, index: int) -> LootPool:
        return self.pools[index]

    def jsonify(self) -> dict:
        data = {"pools": [x.jsonify() for x in self.pools]}
        if self.functions:
            data["functions"] = [x.jsonify() for x in self.functions]
        return data

    @property
    def pools(self) -> list[LootPool]:
        return getattr2(self, "_pools", [])

    @pools.setter
    def pools(self, value: list[LootPool]):
        if value is None:
            self.pools = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("pools", value)
        setattr(self, "_pools", value)

    @property
    def functions(self) -> list[LootFunction]:
        return getattr2(self, "_functions", [])

    @functions.setter
    def functions(self, value: list[LootFunction]):
        if value is None:
            self.functions = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("functions", value)
        setattr(self, "_functions", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "pools" in data:
            self.pools = [LootPool.from_dict(x) for x in data.pop("pools")]

        if "functions" in data:
            v = []
            for x in data.pop("functions"):
                id = x.get("function")
                clazz = INSTANCE.get_registry(Registries.LOOT_FUNCTION_TYPE).get(id)
                if clazz is None:
                    raise TypeNotFoundError(repr(id))
                v.append(clazz.from_dict(x))
            self.functions = v
        return self

    @classmethod
    def block(cls, obj: Identifiable):
        if not isinstance(obj, (Item, Block, Identifier, str)):
            raise TypeError(
                f"Expected Item, Block, or Identifier but got '{obj.__class__.__name__}' instead"
            )
        id = Identifiable.of(obj)
        self = cls.__new__(cls)
        self.identifier = Identifier.of("blocks/" + id.path)
        self.filename = id.path
        pool = LootPool()
        pool.add_entry(ItemEntry(id))
        self.add_pool(pool)
        return self

    def get_pool(self, index: int) -> LootPool:
        return getitem(self, "pools", index)

    def add_pool(self, pool: LootPool) -> LootPool:
        return additem(self, "pools", pool, type=LootPool)

    def remove_pool(self, index: int) -> LootPool:
        return removeitem(self, "pools", index)

    def clear_pools(self) -> Self:
        """Remove all pools"""
        return clearitems(self, "pools")

    def get_function(self, index: int) -> LootFunction:
        return getitem(self, "functions", index)

    def add_function(self, function: LootFunction) -> LootFunction:
        return additem(self, "functions", function, type=LootFunction)

    def remove_function(self, index: int) -> LootFunction:
        return removeitem(self, "functions", index)

    def clear_functions(self) -> Self:
        """Remove all functions"""
        return clearitems(self, "functions")

    def valid(self, fp: str) -> bool:
        return True

    @classmethod
    def open(cls, fp: str, start):
        with open(fp, "r") as fd:
            self = cls.load(fd)
            self.identifier = os.path.relpath(fp, start).replace("\\", "/")
            return self
