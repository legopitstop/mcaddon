__all__ = ["PotionBrewingMixRecipe"]

from typing import List
from mcaddon.core.base import ItemLike, Ingredient
from .base import BaseRecipe

class PotionBrewingMixRecipe(BaseRecipe):
    input: Ingredient | str
    reagent: Ingredient | str
    output: ItemLike
    tags: List[str] = ...
