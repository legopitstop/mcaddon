from mcaddon import *

rpe1 = FurnaceRecipe("furnace_beef", ItemStack("beef"), ItemStack("cooked_beef"))
rpe1.save("build/")

rpe2 = BrewingContainerRecipe(
    "brew_potion_sulphur",
    ItemStack("potion"),
    ItemStack("gunpowder"),
    ItemStack("splash_potion"),
)
rpe2.save("build/")

rpe3 = BrewingMixRecipe(
    "brew_awkward_blaze_powder",
    ItemStack("potion_type"),
    ItemStack("blaze_powder"),
    ItemStack("potion_type"),
)
rpe3.save("build/")

rpe4 = ShapedRecipe("acacia_boat", ["#P#", "###"], ItemStack("boat", data=4))
rpe4.add_key("#", ItemStack("planks"))
rpe4.add_key("P", ItemStack("wooden_shovel"))
rpe4.save("build/")

rpe5 = ShapelessRecipe("firecharge_coal_sulphur", ItemStack("blaze_powder", data=4))
rpe5.add_ingredient(ItemStack("fireball", 4, 0))
rpe5.save("build/")

rpe6 = SmithingTransformRecipe(
    "smithing_netherite_boots",
    ItemStack("netherite_upgrade_smithing_template"),
    ItemStack("diamond_boots"),
    ItemStack("netherite_ingot"),
    ItemStack("netherite_boots"),
)
rpe6.save("build/")

rpe7 = SmithingTrimRecipe(
    "smithing_diamond_boots_jungle_quartz_trim",
    ItemStack("jungle_temple_smithing_template"),
    ItemStack("diamond_boots"),
    ItemStack("quartz"),
)
rpe7.save("build/")
