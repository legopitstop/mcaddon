from mcaddon import SmithingTransformRecipe, ItemStack
from mcaddon.core.base import Ingredient

recipe = SmithingTransformRecipe(
    template=Ingredient(item="apple"),
    base=Ingredient(item="apple"),
    addition=Ingredient(item="apple"),
    result=ItemStack(item="apple", count=2),
)
recipe.save("out/smithing_transform.json")
