from mcaddon import LootTable
from mcaddon.library.loot_entry.item import ItemLootEntry
from mcaddon.library.loot_table import LootPool

loot = LootTable.block("apple")
loot.save("out/loot_table_block.json")

loot = LootTable()
pool = LootPool()
entry = ItemLootEntry(name="apple")
pool.entries.append(entry)
loot.pools.append(pool)
loot.save("out/loot_table.json")
