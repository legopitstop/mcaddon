from mcaddon import ShapelessRecipe, ItemStack
from mcaddon.core.base import Ingredient

recipe = ShapelessRecipe(result=ItemStack(item="apple", count=2))
recipe.description.identifier = "minecraft:apple"
recipe.ingredients.append(Ingredient(item="apple"))
recipe.tags = ["stonecutter"]
recipe.save("out/stonecutter.json")
