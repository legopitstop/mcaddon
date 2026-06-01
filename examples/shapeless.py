from mcaddon import ShapelessRecipe, ItemStack
from mcaddon.core.base import Ingredient

recipe = ShapelessRecipe(result=ItemStack(item="apple", count=2))
recipe.description.identifier = "minecraft:apple"
recipe.ingredients.append(Ingredient(item="apple"))
recipe.save("out/shapeless.json")
