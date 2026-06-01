from mcaddon import FurnaceRecipe, ItemStack
from mcaddon.core.base import Ingredient

recipe = FurnaceRecipe(
    input=Ingredient(item="apple"), output=ItemStack(item="apple", count=2)
)
recipe.save("out/furnace.json")
