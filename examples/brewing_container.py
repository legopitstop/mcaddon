from mcaddon import PotionBrewingRecipe, ItemStack
from mcaddon.core.base import Ingredient

recipe = PotionBrewingRecipe(
    input=Ingredient(item="apple"),
    reagent=Ingredient(item="apple"),
    output=ItemStack(item="apple", count=2),
)
recipe.save("out/brewing_container.json")
