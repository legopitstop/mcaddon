__all__ = ["LootFunction", "BaseLootFunction"]

from abc import ABC
from typing import ClassVar, Dict, Type, Any

from pydantic_core import core_schema
from mcaddon.core.base import BaseModel


class BaseLootFunction(ABC, BaseModel):
    TYPE_ID: ClassVar[str] = "unknown"
    function: str = TYPE_ID

    def __hash__(self) -> int:
        return hash(self.TYPE_ID)


class LootFunction(ABC, BaseModel):
    __all__: ClassVar[Dict[str, Type["LootFunction"]]] = {}

    @classmethod
    def register(cls, clazz: Type["BaseLootFunction"]) -> Type["BaseLootFunction"]:
        def wrapper() -> Type["BaseLootFunction"]:
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
            discriminator="function",
        )
