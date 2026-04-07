__all__ = ["FurnaceRecipe"]

from typing import List
from pydantic import Field

from mcaddon.core.base import ItemLike, Ingredient
from .base import Recipe, BaseRecipe


@Recipe.register
class FurnaceRecipe(BaseRecipe):
    TYPE_ID = "minecraft:recipe_furnace"

    input: Ingredient | str
    output: ItemLike
    tags: List[str] = Field(default=["furnace"])

    @property
    def id(self) -> str:
        return self.description.identifier
