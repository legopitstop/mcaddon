__all__ = ["SmithingTrimRecipe"]

from typing import List

from mcaddon.core.base import Ingredient
from .base import BaseRecipe

class SmithingTrimRecipe(BaseRecipe):
    template: Ingredient | str
    base: Ingredient | str
    addition: Ingredient | str
    tags: List[str] = ...
