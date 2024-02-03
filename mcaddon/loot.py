from typing import Self

from .exception import TypeNotFoundError
from .constant import Destination, LootContextType
from .registry import INSTANCE, Registries
from .file import JsonFile
from .util import getattr2, Identifier, Identifiable
from .block import Block
from .item import Item


class LootNumberProvider:
    def __init__(self, min: float, max: float = None):
        """
        :param min: the minimum value
        :type min: float
        :param max: the maximum value, defaults to None
        :type max: float, optional
        """
        self.min = min
        self.max = max

    @property
    def __dict__(self) -> dict:
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
        setattr(self, "_min", float(value))

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
        setattr(self, "_max", float(value))


class Enchant:
    def __init__(self, id: Identifier, levels: LootNumberProvider):
        """
        An enchantment

        :param id: an enchantment ID
        :type id: Identifier
        :param levels: the level of the enchantment
        :type levels: LootNumberProvider
        """
        self.id = id
        self.levels = levels

    @property
    def __dict__(self) -> dict:
        data = {
            "id": str(self.id),
            "levels": {"range_min": self.levels.min, "range_max": self.levels.max},
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


# CONDITIONS
#  https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable


class LootCondition:
    @property
    def __dict__(self) -> dict:
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
class HasMarkvariantLootCondition(LootCondition):
    id = Identifier("has_mark_variant")

    def __init__(self, value: int):
        """
        Specifies that there are different variations for the loot
        """
        self.value = value

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        setattr(self, "_chance", float(value))


@loot_condition
class RandomChanceWithLootingLootCondition(LootCondition):
    id = Identifier("random_chance_with_looting")

    def __init__(self, chance: float, looting_multiplier: float):
        """
        Similar to the random_chance condition, but also includes a multiplier value
        """
        self.chance = chance
        self.looting_multiplier = looting_multiplier

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        setattr(self, "_chance", float(value))

    @property
    def looting_multiplier(self) -> float:
        return getattr(self, "_looting_multiplier")

    @looting_multiplier.setter
    def looting_multiplier(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_looting_multiplier", float(value))


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

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        setattr(self, "_default_chance", float(value))

    @property
    def peaceful(self) -> float:
        return getattr(self, "_peaceful")

    @peaceful.setter
    def peaceful(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_peaceful", float(value))

    @property
    def hard(self) -> float:
        return getattr(self, "_hard")

    @hard.setter
    def hard(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_hard", float(value))


@loot_condition
class RandomRegionalDifficultyChanceLootCondition(LootCondition):
    id = Identifier("random_regional_difficulty_chance")

    def __init__(self, max_chance: float):
        """
        Determines loot probability according to the region.
        """
        self.max_chance = max_chance

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        setattr(self, "_max_chance", float(value))


@loot_condition
class MatchToolLootCondition(LootCondition):
    id = Identifier("match_tool")

    def __init__(
        self,
        item: Identifier,
        count: LootNumberProvider,
        durability: LootNumberProvider,
        enchantments: list[Enchant],
    ):
        """
        Checks whether the tool (or weapon/item the player is using) used to make the loot drop matches the modifier conditions provided. The predicates used are: count, durability, enchantments, and item

        :param item: An item ID
        :type item: Identifier
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

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
            data["enchantments"] = [x.__dict__ for x in self.enchantments]
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
    def item(self, value: Identifier):
        if not isinstance(value, Identifier):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_item", value)

    @property
    def count(self) -> LootNumberProvider:
        return getattr(self, "_count")

    @count.setter
    def count(self, value: LootNumberProvider):
        if not isinstance(value, LootNumberProvider):
            raise TypeError(
                f"Expected LootNumberProvider but got '{value.__class__.__name__}' instead"
            )
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
        setattr(self, "_enchantments", value)


@loot_condition
class KilledByEntityLootCondition(LootCondition):
    id = Identifier("killed_by_entity")

    def __init__(self, entity_type: Identifier):
        self.entity_type = entity_type

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
    def entity_type(self, value: Identifier):
        if not isinstance(value, Identifier):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_entity_type", value)


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


class LootFunction:
    @property
    def __dict__(self) -> dict:
        data = {"function": str(self.id)}
        return data


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

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        setattr(self, "_per_level_cost", value)


@loot_function
class EnchantRandomGearLootFunction(LootFunction):
    id = Identifier("enchant_random_gear")

    def __init__(self, chance: float):
        """
        Enchants an item utilizing the same algorithm used while enchanting equipment vanilla mobs spawn with. Takes a chance modifier to manipulate the algorithm. Note that a chance modifier of 1.0 doesn't mean a 100% chance that gear will become enchanted. Rather, the chance is modified based on the difficulty. On Peaceful and Easy difficulties, the chance will always be 0% no matter what. On Hard difficulty, a chance of 1.0 will be 100%, but the chance is roughly 2/3 that on Normal difficulty
        """
        self.chance = chance

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        setattr(self, "_chance", float(value))


@loot_function
class EnchantRandomlyLootFunction(LootFunction):
    id = Identifier("enchant_randomly")

    def __init__(self, treasure: bool):
        """
        Generates a random enchantment that is compatible with the item. Supports the optional treasure boolean (true/false) to allow treasure enchantments to be toggled on and off. Treasure enchantments are enchantments that cannot be obtained through the enchanting table, including Frost Walker, Mending, Soul Speed, Curse of Binding, and Curse of Vanishing
        """
        self.treasure = treasure

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data["treasure"] = self.treasure
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.treasure = data.pop("treasure")
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

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data["treasure"] = self.treasure
        data["levels"] = self.levels.__dict__
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
        setattr(self, "_levels", value)


@loot_function
class SpecificEnchantsLootFunction(LootFunction):
    id = Identifier("specific_enchants")

    def __init__(self, enchants: list[Identifier | Enchant]):
        """
        This function allows you to set a list of specific enchantments on an item. It also allows you to apply enchantments to items that wouldn't normally be enchantable in-game.
        """
        self.enchants = enchants

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data["enchants"] = [x.__dict__ for x in self.enchants]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.enchants = [Enchant.from_dict(x) for x in data.pop("enchants")]
        return self

    @property
    def enchantments(self) -> list[Identifier | Enchant]:
        return getattr(self, "_enchantments")

    @enchantments.setter
    def enchantments(self, value: list[Identifier | Enchant]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_enchantments", value)


# loot table only
@loot_function
class LootingEnchantLootFunction(LootFunction):
    id = Identifier("looting_enchant")

    def __init__(self, count: LootNumberProvider):
        """
        This function allows you to modify the count of how many items are returned when an entity is killed by an item with the looting enchantment. Due to that, it only works with loot tables, and only if that loot table is called by the death of an entity.
        """
        self.count = count

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data["count"] = self.count.__dict__
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
        setattr(self, "_count", value)


@loot_function
class RandomAuxValueLootFunction(LootFunction):
    id = Identifier("random_aux_value")

    def __init__(self, values: LootNumberProvider):
        """
        Similar to random_block_state, this allows you to pick a random auxiliary value for an item. The following example will result in a randomly-colored dye.
        """
        self.values = values

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data["values"] = self.values.__dict__
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
        setattr(self, "_values", value)


@loot_function
class RandomBlockStateLootFunction(LootFunction):
    id = Identifier("random_block_state")

    def __init__(self, block_state: Identifier, values: LootNumberProvider):
        """
        This allows you to randomize the block state of the resulting item. For instance, the following example code can drop stone (0), granite (1), polished granite (2), diorite (3), polished diorite (4), or andesite (5).
        """
        self.block_state = block_state
        self.values = values

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data["block_state"] = str(self.block_state)
        data["values"] = self.values.__dict__
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
    def block_state(self, value: Identifier):
        if not isinstance(value, (Identifier, str)):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_block_state", Identifier(value))

    @property
    def values(self) -> LootNumberProvider:
        return getattr(self, "_values")

    @values.setter
    def values(self, value: LootNumberProvider):
        if not isinstance(value, LootNumberProvider):
            raise TypeError(
                f"Expected LootNumberProvider but got '{value.__class__.__name__}' instead"
            )
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

    def __init__(self, actor_id: Identifier):
        """
        This function only works with a spawn egg and is used to set the entity ID of that spawn egg.
        """
        self.actor_id = actor_id

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
    def actor_id(self, value: Identifier):
        if not isinstance(value, (Identifier, str)):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_actor_id", Identifier(value))


@loot_function
class SetBannerDetailsLootFunction(LootFunction):
    id = Identifier("set_banner_details")

    def __init__(self, type: int):
        """
        This function only works on banners and currently only supports a banner type of 1. A banner type of 1 results in an illager banner.
        """
        self.type = type

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        setattr(self, "_author", str(value))

    @property
    def title(self) -> str:
        return getattr(self, "_title")

    @title.setter
    def title(self, value: str):
        setattr(self, "_title", str(value))

    @property
    def pages(self) -> list[str]:
        return getattr(self, "_pages")

    @pages.setter
    def pages(self, value: list[str]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_pages", value)


@loot_function
class SetCountLootFunction(LootFunction):
    id = Identifier("set_count")

    def __init__(self, count: LootNumberProvider):
        """
        Sets the quantity of items returned by setting the count value
        """
        self.count = count

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data["count"] = self.count.__dict__
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
        setattr(self, "_count", value)


@loot_function
class SetDamageLootFunction(LootFunction):
    id = Identifier("set_damage")

    def __init__(self, damage: LootNumberProvider):
        """
        Sets the percentage of durability remaining for items that have durability by setting the damage value. 1.0 is 100% of durability remaining (undamaged) while 0.0 is no durability remaining.
        """
        self.damage = damage

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data["damage"] = self.damage.__dict__
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
        setattr(self, "_damage", value)


@loot_function
class SetDataLootFunction(LootFunction):
    id = Identifier("set_data")

    def __init__(self, data: int):
        """
        Sets the data value of a block or item to an exact id. This is useful for things like returning a specific potion or specific color of item. It also allows you to return different block values, like a specific log type
        """
        self.data = data

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
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

    def __init__(self, lore: list[str]):
        """
        This function allows you to set the lore of an item. Each line within the lore object represents a single line of text. There's currently no support for rawtext.
        """
        self.lore = lore

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        setattr(self, "_lore", value)


@loot_function
class SetNameLootFunction(LootFunction):
    id = Identifier("set_name")

    def __init__(self, name: str):
        """
        This function allows you to set the name of an item. There's currently no support for rawtext.
        """
        self.name = name

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        setattr(self, "_name", str(value))


@loot_function
class ExplorationMapLootFunction(LootFunction):
    id = Identifier("exploration_map")

    def __init__(self, destination: Destination):
        """
        Transforms a normal map into a treasure map that marks the location of hidden treasure. The destination value defines what type of treasure map they receive.
        """
        self.destination = destination

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data["destination"] = self.destination._value_
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.destination = Destination[data.pop("destination")]
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

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        setattr(self, "_loot_table", str(value))


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


class LootPoolEntry:
    def __init__(self, conditions: list[LootCondition] = None):
        self.conditions = conditions

    @property
    def __dict__(self) -> dict:
        data = {"type": str(self.id.path)}
        if self.conditions:
            data["conditions"] = [x.__dict__ for x in self.conditions]
        return data

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
        setattr(self, "_conditions", value)

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        if not isinstance(value, Identifier):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_id", value)

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
        conditions: list[LootCondition] = None,
        functions: list[LootFunction] = None,
    ):
        LootPoolEntry.__init__(self, conditions)
        self.weight = weight
        self.quality = quality
        self.functions = functions

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        if self.weight not in [None, 1]:
            data["weight"] = self.weight
        if self.quality not in [None, 1]:
            data["quality"] = self.quality
        if self.functions:
            data["functions"] = [x.__dict__ for x in self.functions]
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

    def get_condition(self, index: int) -> LootCondition:
        return self.conditions[index]

    def add_condition(self, condition: LootCondition) -> LootCondition:
        if not isinstance(condition, LootCondition):
            raise TypeError(
                f"Expected LootCondition but got '{function.__class__.__name__}' instead"
            )
        self.conditions.append(condition)
        return condition

    def remove_condition(self, index: int) -> LootCondition:
        return self.conditions.pop(index)

    def clear_conditions(self) -> Self:
        self.conditions = []
        return self

    def get_function(self, index: int) -> LootFunction:
        return self.functions[index]

    def add_function(self, function: LootFunction) -> LootFunction:
        if not isinstance(function, LootFunction):
            raise TypeError(
                f"Expected LootFunction but got '{function.__class__.__name__}' instead"
            )
        self.functions.append(function)
        return function

    def remove_function(self, index: int) -> LootFunction:
        return self.functions.pop(index)

    def clear_functions(self) -> Self:
        self.functions = []
        return self


@pool_entry
class ItemEntry(LeafEntry):
    id = Identifier("item")

    def __init__(
        self,
        name: Identifier,
        weight: int = None,
        quality: int = None,
        conditions: list[LootCondition] = None,
        functions: list[LootFunction] = None,
    ):
        LeafEntry.__init__(self, weight, quality, conditions, functions)
        self.name = name

    def __str__(self) -> str:
        return "ItemEntry{" + str(self.item) + "}"

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data["name"] = str(self.name)
        return data

    @property
    def name(self) -> Identifier:
        return getattr(self, "_name")

    @name.setter
    def name(self, value: Identifier):
        if not isinstance(value, (Identifier, str)):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_name", Identifier(value))

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
        conditions: list[LootCondition] = None,
        functions: list[LootFunction] = None,
    ):
        LeafEntry.__init__(self, weight, quality, conditions, functions)
        self.name = name

    def __str__(self) -> str:
        return "LootEntry{" + repr(self.name) + "}"

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data["name"] = self.name
        return data

    @property
    def name(self) -> str:
        return getattr(self, "_name")

    @name.setter
    def name(self, value: str):
        setattr(self, "_name", str(value))

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        if "name" in data:
            self.name = data.pop("name")
        return self


# MISC


class LootTiers:
    def __init__(self, initial_range: int, bonus_rolls: int, bonus_chance: float):
        self.initial_range = initial_range
        self.bonus_rolls = bonus_rolls
        self.bonus_chance = bonus_chance

    @property
    def __dict__(self) -> dict:
        data = {
            "initial_range": self.initial_range,
            "bonus_rolls": self.bonus_rolls,
            "bonus_chance": self.bonus_chance,
        }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.initial_range = data.pop("initial_range")
        self.bonus_rolls = data.pop("bonus_rolls")
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
        setattr(self, "_initial_range", value)

    @property
    def bonus_rolls(self) -> int:
        return getattr(self, "_bonus_rolls")

    @bonus_rolls.setter
    def bonus_rolls(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_bonus_rolls", value)

    @property
    def bonus_chance(self) -> float:
        return getattr(self, "_bonus_chance")

    @bonus_chance.setter
    def bonus_chance(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_bonus_chance", float(value))


class LootPool:
    def __init__(
        self,
        rolls: LootNumberProvider = None,
        bonus_rolls: LootNumberProvider = None,
        tiers: LootTiers = None,
        entries: list[LootPoolEntry] = None,
        conditions: list[LootCondition] = None,
        functions: list[LootFunction] = None,
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

    @property
    def __dict__(self) -> dict:
        data = {"entries": [x.__dict__ for x in self.entries]}
        if self.tiers:
            data["tiers"] = self.tiers.__dict__
        if self.conditions:
            data["conditions"] = [x.__dict__ for x in self.conditions]
        if self.functions:
            data["functions"] = [x.__dict__ for x in self.functions]
        if self.rolls not in [None, 1.0]:
            data["rolls"] = self.rolls.__dict__
        if self.bonus_rolls not in [None, 1.0]:
            data["bonus_rolls"] = self.bonus_rolls.__dict__
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
        return self.entries[index]

    def add_entry(self, function: LootPoolEntry) -> LootPoolEntry:
        if not isinstance(function, LootPoolEntry):
            raise TypeError(
                f"Expected LootPoolEntry but got '{function.__class__.__name__}' instead"
            )
        self.entries.append(function)
        return function

    def remove_entry(self, index: int) -> LootPoolEntry:
        return self.entries.pop(index)

    def clear_entries(self) -> Self:
        self.entries = []
        return self

    def get_condition(self, index: int) -> LootCondition:
        return self.conditions[index]

    def add_condition(self, function: LootCondition) -> LootCondition:
        if not isinstance(function, LootCondition):
            raise TypeError(
                f"Expected LootCondition but got '{function.__class__.__name__}' instead"
            )
        self.conditions.append(function)
        return function

    def remove_condition(self, index: int) -> LootCondition:
        return self.conditions.pop(index)

    def clear_conditions(self) -> Self:
        self.conditions = []
        return self

    def get_function(self, index: int) -> LootFunction:
        return self.functions[index]

    def add_function(self, function: LootFunction) -> LootFunction:
        if not isinstance(function, LootFunction):
            raise TypeError(
                f"Expected LootFunction but got '{function.__class__.__name__}' instead"
            )
        self.functions.append(function)
        return function

    def remove_function(self, index: int) -> LootFunction:
        return self.functions.pop(index)

    def clear_functions(self) -> Self:
        self.functions = []
        return self


class LootTable(JsonFile, Identifiable):
    extension = ".json"
    filename = "loot_table"
    dirname = "loot_tables"

    def __init__(
        self,
        type: LootContextType = None,
        pools: list[LootPool] = None,
        functions: list[LootFunction] = None,
    ):
        Identifiable.__init__(self, "empty.json")
        self.type = type
        self.pools = pools
        self.functions = functions

    def __iter__(self):
        for pool in self.pools:
            yield pool

    def __getitem__(self, index: int) -> LootPool:
        return self.pools[index]

    @property
    def __dict__(self) -> dict:
        data = {"pools": [x.__dict__ for x in self.pools]}
        if self.type not in [None, LootContextType.empty]:
            data["type"] = self.type._value_
        if self.functions:
            data["functions"] = [x.__dict__ for x in self.functions]
        return data

    @property
    def type(self) -> LootContextType:
        return getattr2(self, "_type", LootContextType.empty)

    @type.setter
    def type(self, value: LootContextType):
        if value is None:
            self.type = LootContextType.empty
            return
        if not isinstance(value, LootContextType):
            raise TypeError(
                f"Expected LootContextType but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_type", value)

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
        setattr(self, "_functions", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.pools = [LootPool.from_dict(x) for x in data.pop("pools")]
        if "type" in data:
            self.type = LootContextType[data.pop("type")]

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
    def block(cls, obj: Item | Block | Identifier | str):
        if not isinstance(obj, (Item, Block, Identifier, str)):
            raise TypeError(
                f"Expected Item, Block, or Identifier but got '{obj.__class__.__name__}' instead"
            )
        id = None
        if isinstance(obj, (Block, Item)):
            id = obj.id
        if isinstance(obj, (Identifier, str)):
            id = Identifier(obj)
        self = cls.__new__(cls)
        self.identifier = Identifier("blocks/" + id.path)
        self.filename = id.path
        pool = LootPool()
        pool.add_entry(ItemEntry(id))
        self.add_pool(pool)
        return self

    def get_pool(self, index: int) -> LootPool:
        return self.pools[index]

    def add_pool(self, pool: LootPool) -> LootPool:
        if not isinstance(pool, LootPool):
            raise TypeError(
                f"Expected LootPool but got '{pool.__class__.__name__}' instead"
            )
        self.pools.append(pool)
        return pool

    def remove_pool(self, index: int) -> LootPool:
        return self.pools.pop(index)

    def clear_pools(self) -> Self:
        self.pools = []
        return self

    def get_function(self, index: int) -> LootFunction:
        return self.functions[index]

    def add_function(self, function: LootFunction) -> LootFunction:
        if not isinstance(function, LootFunction):
            raise TypeError(
                f"Expected LootFunction but got '{function.__class__.__name__}' instead"
            )
        self.functions.append(function)
        return function

    def remove_function(self, index: int) -> LootFunction:
        return self.functions.pop(index)

    def clear_functions(self) -> Self:
        self.functions = []
        return self
