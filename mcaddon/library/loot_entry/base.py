__all__ = [
    "LootEntry",
    "LootFunction",
    "LootCondition",
]

from typing import ClassVar, Dict, Optional, Any, Type
from pydantic_core import core_schema
from abc import ABC

from mcaddon.core.base import BaseModel
from mcaddon.library.loot_function import LootFunction
from mcaddon.library.loot_condition import LootCondition


class LootEntry(ABC, BaseModel):
    __all__: ClassVar[Dict[str, Type["LootEntry"]]] = {}

    TYPE_ID: ClassVar[str] = "unknown"
    type: str = TYPE_ID

    weight: Optional[int] = None
    count: Optional[int] = None

    def __hash__(self) -> int:
        return hash(self.TYPE_ID)

    @classmethod
    def register(cls, clazz: Type["LootEntry"]) -> Type["LootEntry"]:
        def wrapper() -> Type["LootEntry"]:
            if hasattr(cls, "__all__"):
                all = getattr(cls, "__all__")
                if clazz.TYPE_ID in all:
                    msg = f"{cls.__name__} '{clazz.TYPE_ID}' was already registered!"
                    raise Exception(msg)
                all[clazz.TYPE_ID] = clazz
            return clazz

        return wrapper()

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Any, handler):
        choices = {}

        for id, c in cls.__all__.items():
            choices[id] = handler(c)

        return core_schema.tagged_union_schema(
            choices=choices,
            discriminator="type",
        )
