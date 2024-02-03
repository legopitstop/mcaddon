from mcaddon import Item, Addon

with Addon.load("build/addon") as addon:
    addon.add(Item("test"))
