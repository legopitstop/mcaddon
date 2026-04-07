__all__ = ["ShapedRecipe"]

from typing import List, Optional, Dict
from pydantic import Field

from mcaddon.core.base import ItemLike, Ingredient
from .base import Recipe, BaseRecipe


@Recipe.register
class ShapedRecipe(BaseRecipe):
    TYPE_ID = "minecraft:recipe_shaped"

    result: ItemLike | List[ItemLike] = Field(default_factory=list)
    pattern: List[str] = Field(default_factory=list)
    key: Dict[str, Ingredient] = Field(default_factory=dict)
    priority: Optional[int] = None
    assume_symmetry: Optional[bool] = None
    tags: List[str] = Field(default=["crafting_table"])

    @property
    def id(self) -> str:
        return self.description.identifier
