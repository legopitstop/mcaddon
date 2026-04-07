__all__ = ["FurnaceRecipe"]

from typing import List
from mcaddon.core.base import ItemLike, Ingredient
from .base import BaseRecipe

class FurnaceRecipe(BaseRecipe):
    input: Ingredient | str
    output: ItemLike
    tags: List[str] = ...
