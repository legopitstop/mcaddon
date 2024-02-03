from mcaddon import Item

itm = Item.load("build/item.json")
print(itm.identifier)
itm.save("build/output.json")
