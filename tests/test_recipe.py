from mcaddon import *

rpe1 = FurnaceRecipe(
    "furnace_beef", Ingredient(ItemStack("beef")), ItemStack("cooked_beef")
)

rpe2 = BrewingContainerRecipe(
    "brew_potion_sulphur",
    ItemStack("potion"),
    ItemStack("gunpowder"),
    ItemStack("splash_potion"),
)

rpe3 = BrewingMixRecipe(
    "brew_awkward_blaze_powder",
    ItemStack("potion_type"),
    ItemStack("blaze_powder"),
    ItemStack("potion_type"),
)

rpe4 = ShapedRecipe("acacia_boat", ItemStack("boat", data=4), ["#P#", "###"])
rpe4.add_key("#", ItemStack("planks"))
rpe4.add_key("P", ItemStack("wooden_shovel"))

rpe5 = ShapelessRecipe("firecharge_coal_sulphur", ItemStack("blaze_powder", data=4))
rpe5.add_ingredient(ItemStack("fireball", 4, 0))

rpe6 = SmithingTransformRecipe(
    "smithing_netherite_boots",
    ItemStack("netherite_upgrade_smithing_template"),
    ItemStack("diamond_boots"),
    ItemStack("netherite_ingot"),
    ItemStack("netherite_boots"),
)

rpe7 = SmithingTrimRecipe(
    "smithing_diamond_boots_jungle_quartz_trim",
    Ingredient(ItemStack("jungle_temple_smithing_template")),
    Ingredient(ItemStack("diamond_boots")),
    Ingredient(ItemStack("quartz")),
)

rpe1.save("build/")
rpe2.save("build/")
rpe3.save("build/")
rpe4.save("build/")
rpe5.save("build/")
rpe6.save("build/")
rpe7.save("build/")

recipes = [rpe1, rpe2, rpe3, rpe4, rpe5, rpe6, rpe7]
