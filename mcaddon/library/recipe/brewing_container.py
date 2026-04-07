__all__ = ["PotionBrewingRecipe"]

from typing import List
from pydantic import Field

from mcaddon.core.base import ItemLike, Ingredient
from .base import BaseRecipe, Recipe


@Recipe.register
class PotionBrewingRecipe(BaseRecipe):
    TYPE_ID = "minecraft:recipe_brewing_container"

    input: Ingredient | str
    reagent: Ingredient | str
    output: ItemLike
    tags: List[str] = Field(default=["brewing_stand"])
