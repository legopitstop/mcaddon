from mcaddon import *

trde = Trading("minister")
tier1 = TradeTier()

group = TradeGroup(1)
gives1 = ItemTrade("enchanted_book")
gives1.add_function(EnchantBookForTradingLootFunction(4, 12, 8, 4))
group.add_trade(
    Trade(
        [
            ItemTrade("wiki:blessing_glyph", Range(2, 4), price_multiplier=0.5),
            ItemTrade("book"),
        ],
        gives1,
        7,
        3,
    )
)

gives2 = ItemTrade("wiki:exalted_blade")
gives2.add_function(EnchantWithLevelsLootFunction(True, LootNumberProvider(15, 25)))
group.add_trade(
    Trade(
        ItemTrade("wiki:crystalline_spiritite", 32, price_multiplier=0.125),
        gives2,
        2,
        8,
        False,
    )
)

tier1.add_group(group)
trde.add_tier(tier1)

# tier2 = TradeTier(28)
# tier2.add_trade(Trade())
# tier2.add_trade(Trade())
# trde.add_tier(tier2)

trde.save("build/")
