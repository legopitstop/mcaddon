from mcaddon import *

biome_filter = Filters()
biome_filter.add_filter(Filter("has_biome_tag", "forest", "=="))
all_of = AllFilter()
all_of.add_filter(Filter("has_biome_tag", "birch", "=="))
all_of.add_filter(Filter("has_biome_tag", "mutated", "!="))
biome_filter.add_filter(all_of)

conditions = FeatureRuleCondition("surface_pass", biome_filter)
rule = FeatureRule(
    "minecraft:birch_forest_surface_trees_feature",
    "minecraft:legacy:birch_forest_tree_feature",
    conditions,
    Distribution(1, 0, 0, 0),
)
rule.save("build/")
