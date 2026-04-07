__all__ = ["LootTable", "LootEntry", "BaseLootEntry", "LootFunction", "LootCondition"]

from typing import ClassVar, Dict, List, Optional, Any, Type
from pydantic import Field
from pydantic_core import core_schema
from abc import ABC

from mcaddon.core.file import JsonFile
from mcaddon.core.base import BaseModel, NumberRange
from mcaddon.core.utils import namespaced
from mcaddon.library.loot_function import LootFunction
from mcaddon.library.loot_condition import LootCondition
from .pack import behaviorpack


class BaseLootEntry(ABC, BaseModel):
    TYPE_ID: ClassVar[str] = "unknown"
    type: str = TYPE_ID

    weight: Optional[int] = None
    count: Optional[int] = None

    def __hash__(self) -> int:
        return hash(self.TYPE_ID)


class LootEntry(ABC, BaseModel):
    __all__: ClassVar[Dict[str, Type["LootEntry"]]] = {}

    @classmethod
    def register(cls, clazz: Type["BaseLootEntry"]) -> Type["BaseLootEntry"]:
        def wrapper() -> Type["BaseLootEntry"]:
            if hasattr(cls, "__all__"):
                all = getattr(cls, "__all__")
                if clazz.TYPE_ID in all:
                    msg = f"{cls.__name__} '{clazz.TYPE_ID}' was already registered!"
                    raise Exception(msg)
                all[clazz.TYPE_ID] = clazz
            return clazz

        return wrapper()

    # @classmethod
    # def model_entries(cls, obj):
    #     entries = []
    #     all = getattr(cls, "__all__")

    #     for v in obj:
    #         id = v.get("type")
    #         entry = all.get(id)
    #         if entry is None:
    #             raise ValueError(f"Unknown loot entry '{id}'")
    #         try:
    #             del v["type"]
    #             entries.append(entry.model_validate(v))
    #         except ValidationError as err:
    #             print(id)
    #             raise err
    #     return entries

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Any, handler):
        choices = {}

        for id, c in cls.__all__.items():
            choices[namespaced(id)] = handler(c)

        union = core_schema.tagged_union_schema(
            choices=choices,
            discriminator="type",
        )

        return core_schema.chain_schema(
            [
                core_schema.no_info_plain_validator_function(lambda e: namespaced(e)),
                union,
            ]
        )


@LootEntry.register
class ItemLootEntry(BaseLootEntry):
    TYPE_ID = "item"

    name: str
    functions: List[LootFunction] = Field(default_factory=list)
    conditions: List[LootCondition] = Field(default_factory=list)
    pools: List["Pool"] = Field(default_factory=list)


@LootEntry.register
class EmptyLootEntry(BaseLootEntry):
    TYPE_ID = "empty"


@LootEntry.register
class LootTableLootEntry(BaseLootEntry):
    TYPE_ID = "loot_table"

    name: str
    quality: Optional[int] = None


class PoolTiers(BaseModel):
    initial_range: int
    bonus_rolls: Optional[int] = None
    bonus_chance: Optional[float] = None


class Pool(BaseModel):
    rolls: Optional[int | NumberRange] = None
    bonus_rolls: Optional[int | NumberRange] = None
    entries: List[LootEntry] = Field(default_factory=list)
    tiers: Optional[PoolTiers] = None

    functions: List[Any] = Field(default_factory=list)
    conditions: List[Any] = Field(default_factory=list)


@behaviorpack("loot_tables")
class LootTable(JsonFile):
    pools: List[Pool] = Field(default_factory=list)
    type: Optional[str] = None
