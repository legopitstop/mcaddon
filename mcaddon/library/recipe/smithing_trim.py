__all__ = ["SmithingTrimRecipe"]

from typing import List
from pydantic import Field

from mcaddon.core.base import Ingredient
from .base import Recipe, BaseRecipe


@Recipe.register
class SmithingTrimRecipe(BaseRecipe):
    TYPE_ID = "minecraft:recipe_smithing_trim"

    template: Ingredient | str
    base: Ingredient | str
    addition: Ingredient | str
    tags: List[str] = Field(default=["smithing_table"])

    @property
    def id(self) -> str:
        return self.description.identifier
