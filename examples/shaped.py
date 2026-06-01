from mcaddon import ShapedRecipe, ItemStack
from mcaddon.core.base import Ingredient

recipe = ShapedRecipe(
    pattern=["###", "###", "###"], result=ItemStack(item="apple", count=2)
)
recipe.description.identifier = "minecraft:apple"
recipe.key["#"] = Ingredient(item="apple")
recipe.save("out/shaped.json")
