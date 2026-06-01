__all__ = [
    "BaseInputPredicate",
    "InputPredicate",
    "RandomBlockMatchInputPredicate",
    "BlockMatchInputPredicate",
]

from typing import ClassVar, Any, Type, Dict
from pydantic_core import core_schema
from abc import ABC

from mcaddon.core.base import BaseModel
from mcaddon.core.utils import namespaced


class BaseInputPredicate(ABC, BaseModel):
    TYPE_ID: ClassVar[str] = "unknown"
    predicate_type: str = TYPE_ID

    def __hash__(self) -> int:
        return hash(self.TYPE_ID)


class InputPredicate(ABC, BaseModel):
    __all__: ClassVar[Dict[str, Type["InputPredicate"]]] = {}

    @classmethod
    def register(cls, clazz: Type["BaseInputPredicate"]) -> Type["BaseInputPredicate"]:
        def wrapper() -> Type["BaseInputPredicate"]:
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
            choices[namespaced(id)] = handler(c)

        union = core_schema.tagged_union_schema(
            choices=choices,
            discriminator="predicate_type",
        )

        return core_schema.chain_schema(
            [
                core_schema.no_info_plain_validator_function(
                    lambda e: namespaced(e, "predicate_type")
                ),
                union,
            ]
        )


@InputPredicate.register
class RandomBlockMatchInputPredicate(BaseInputPredicate):
    TYPE_ID = "minecraft:random_block_match"
    processor_type: str = TYPE_ID

    block: str
    probability: float


@InputPredicate.register
class BlockMatchInputPredicate(BaseInputPredicate):
    TYPE_ID = "minecraft:block_match"
    processor_type: str = TYPE_ID

    block: str
