__all__ = ["BaseProcessor", "Processor"]

from typing import List, ClassVar, Any, Type, Dict, Optional
from pydantic import Field
from pydantic_core import core_schema
from abc import ABC

from mcaddon.core.base import BaseModel, BlockLike
from mcaddon.core.utils import namespaced
from .predicate_type import InputPredicate
from .block_entity_modifier import BlockEntityModifier


class BaseProcessor(ABC, BaseModel):
    TYPE_ID: ClassVar[str] = "unknown"
    processor_type: str = TYPE_ID

    def __hash__(self) -> int:
        return hash(self.TYPE_ID)


class Processor(ABC, BaseModel):
    __all__: ClassVar[Dict[str, Type["Processor"]]] = {}

    @classmethod
    def register(cls, clazz: Type["BaseProcessor"]) -> Type["BaseProcessor"]:
        def wrapper() -> Type["BaseProcessor"]:
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
            discriminator="processor_type",
        )

        return core_schema.chain_schema(
            [
                core_schema.no_info_plain_validator_function(
                    lambda e: namespaced(e, "processor_type")
                ),
                union,
            ]
        )


class ProcessorRule(BaseModel):
    input_predicate: InputPredicate
    output_state: BlockLike
    block_entity_modifier: Optional[BlockEntityModifier] = None


@Processor.register
class RuleProcessor(BaseProcessor):
    TYPE_ID = "minecraft:rule"
    processor_type: str = TYPE_ID

    rules: List[ProcessorRule] = Field(default_factory=list)


@Processor.register
class CappedProcessor(BaseProcessor):
    TYPE_ID = "minecraft:capped"
    processor_type: str = TYPE_ID

    limit: int
    delegate: Processor
