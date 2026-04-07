__all__ = ["ShapelessRecipe"]

from typing import List, Optional
from pydantic import Field

from mcaddon.core.base import ItemLike, Ingredient
from .base import Recipe, BaseRecipe


@Recipe.register
class ShapelessRecipe(BaseRecipe):
    TYPE_ID = "minecraft:recipe_shapeless"

    result: ItemLike | List[ItemLike] = Field(default_factory=list)
    ingredients: List[Ingredient] = Field(default_factory=list)
    priority: Optional[int] = None
    tags: List[str] = Field(default=["crafting_table"])

    @property
    def id(self) -> str:
        return self.description.identifier
