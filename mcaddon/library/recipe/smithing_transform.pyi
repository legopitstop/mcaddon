__all__ = ["SmithingTransformRecipe"]

from typing import List
from mcaddon.core.base import ItemLike, Ingredient
from .base import BaseRecipe

class SmithingTransformRecipe(BaseRecipe):
    template: Ingredient | str
    base: Ingredient | str
    addition: Ingredient | str
    result: ItemLike
    tags: List[str] = ...
