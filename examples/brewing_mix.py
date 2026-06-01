from mcaddon import PotionBrewingMixRecipe, ItemStack
from mcaddon.core.base import Ingredient

recipe = PotionBrewingMixRecipe(
    input=Ingredient(item="apple"),
    reagent=Ingredient(item="apple"),
    output=ItemStack(item="apple", count=2),
)
recipe.save("out/brewing_mix.json")
