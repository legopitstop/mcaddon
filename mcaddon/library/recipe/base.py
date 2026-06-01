__all__ = ["Recipe", "BaseRecipe"]

from typing import ClassVar, Dict, Type, Any
from pydantic_core import core_schema

from mcaddon.core.file import ResourceFile
from mcaddon.library.common import BaseDescription
from mcaddon.library.pack import behaviorpack


class BaseRecipe(ResourceFile):
    format_version: str = "1.20.10"

    description: BaseDescription = BaseDescription(identifier="minecraft:recipe")

    @property
    def id(self) -> str:
        return self.description.identifier


@behaviorpack("recipes")
class Recipe(ResourceFile):
    __all__: ClassVar[Dict[str, Type["BaseRecipe"]]] = {}
    format_version: str = "1.21.50"

    @classmethod
    def register(cls, clazz: Type["BaseRecipe"]) -> Type["BaseRecipe"]:
        def wrapper() -> Type["BaseRecipe"]:
            if hasattr(cls, "__all__"):
                all = getattr(cls, "__all__")
                if clazz.TYPE_ID in all:
                    msg = f"{cls.__name__} '{clazz.TYPE_ID}' was already registered!"
                    raise Exception(msg)
                all[clazz.TYPE_ID] = clazz
            return clazz

        return wrapper()

    @classmethod
    def _validate_recipe(cls, value: Any) -> BaseRecipe:
        if not isinstance(value, dict):
            raise TypeError("Recipe must be a dict")
        for id, recipe in Recipe.__all__.items():
            if id in value:
                return recipe.model_validate(value)
        raise TypeError(f"Recipe type not found: {value}")

    @classmethod
    def serialize(cls, value: Any) -> Dict[str, Any]:
        if not isinstance(value, Recipe):
            raise TypeError(f"value must be a set, but got '{type(value)}'")
        return {}

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Any, handler):

        return core_schema.no_info_plain_validator_function(
            cls._validate_recipe,
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls.serialize
            ),
        )
