from mcaddon import SmithingTrimRecipe, ItemStack
from mcaddon.core.base import Ingredient

recipe = SmithingTrimRecipe(
    template=Ingredient(item="apple"),
    base=Ingredient(item="apple"),
    addition=Ingredient(item="apple"),
    result=ItemStack(item="apple", count=2),
)
recipe.save("out/smithing_trim.json")
