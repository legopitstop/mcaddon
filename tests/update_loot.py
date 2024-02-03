from mcaddon import LootTable

with LootTable.load("build/loot1.json") as ctx:
    ctx[0].rolls = 0.5
