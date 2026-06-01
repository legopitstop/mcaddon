from mcaddon import (
    Item,
    ItemFuelComponent,
    ItemMaxStackSizeComponent,
    ItemIconComponent,
    ItemHandEquippedComponent,
    ItemDisplayNameComponent,
)

item = Item()
item.description.identifier = "minecraft:blaze_rod"
item.components.add(ItemFuelComponent(duration=12))
item.components.add(ItemMaxStackSizeComponent(value=64))
item.components.add(ItemIconComponent().add("blaze_rod"))
item.components.add(ItemHandEquippedComponent())
item.components.add(ItemDisplayNameComponent(value="Blaze Rod"))
item.save("out/item.json")
