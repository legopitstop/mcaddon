__all__ = ["PotionBrewingMixRecipe"]

from typing import List
from pydantic import Field

from mcaddon.core.base import ItemLike, Ingredient

from .base import Recipe, BaseRecipe


@Recipe.register
class PotionBrewingMixRecipe(BaseRecipe):
    TYPE_ID = "minecraft:recipe_brewing_mix"

    input: Ingredient | str
    reagent: Ingredient | str
    output: ItemLike
    tags: List[str] = Field(default=["brewing_stand"])

    @property
    def id(self) -> str:
        return self.description.identifier
