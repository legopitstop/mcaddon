from mcaddon import (
    LootTable,
    LootPool,
    ItemEntry,
    LootEntry,
    LootNumberProvider,
    LootTiers,
    SetCountLootFunction,
    RandomChanceLootCondition,
)

# Weighted Random Pools
loot1 = LootTable()
pool1 = LootPool(LootNumberProvider(2, 4))
entry1 = ItemEntry("golden_apple", 20)
entry1.add_function(SetCountLootFunction(LootNumberProvider(1, 10)))
entry1.add_condition(RandomChanceLootCondition(0.5))
pool1.add_entry(entry1)
entry2 = ItemEntry("appleEnchanted", 1)
pool1.add_entry(entry2)
entry3 = ItemEntry("name_tag", 30)
pool1.add_entry(entry3)
loot1.add_pool(pool1)
loot1.save("build/loot1.json")

# Tiered Pools
loot2 = LootTable()
pool2 = LootPool(tiers=LootTiers(2, 3, 0.095))
entry1 = LootEntry("loot_tables/entities/armor_set_leather.json")
pool2.add_entry(entry1)
loot2.add_pool(pool2)
loot2.save("build/loot2.json")
