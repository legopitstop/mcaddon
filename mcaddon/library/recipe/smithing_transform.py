__all__ = ["SmithingTransformRecipe"]

from typing import List
from pydantic import Field

from mcaddon.core.base import ItemLike, Ingredient
from .base import Recipe, BaseRecipe


@Recipe.register
class SmithingTransformRecipe(BaseRecipe):
    TYPE_ID = "minecraft:recipe_smithing_transform"

    template: Ingredient | str
    base: Ingredient | str
    addition: Ingredient | str
    result: ItemLike
    tags: List[str] = Field(default=["smithing_table"])

    @property
    def id(self) -> str:
        return self.description.identifier
