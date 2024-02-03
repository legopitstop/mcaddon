"""
All vanilla Minecraft registries located in the vanilla packs.
"""

from enum import Enum

from .. import (
    Item,
    Block,
    CameraPreset,
    Identifier,
    MenuCategory,
    Category,
    FoodComponent,
    IconComponent,
)


class AppleItem(Item):
    def __init__(self, id: Identifier | str):
        Item.__init__(self, id, MenuCategory(Category.items, "itemGroup.name.food"))
        self.add_component(FoodComponent(0, 1.0))
        self.add_component(IconComponent("minecraft:apple"))


class Items(Enum):
    AIR = Item("air")
    APPLE = Item("apple")


class Blocks(Enum):
    AIR = Block("air")


class Cameras(Enum):
    FIRST_PERSON = CameraPreset("first_person")
    FREE = CameraPreset("free", pos_x=0, pos_y=0, pos_z=0, rot_x=0, rot_y=0)
    THIRD_PERSON = CameraPreset("third_person")
    THIRD_PERSON_FRONT = CameraPreset("third_person_front")


# class LootTables(Enum):
#     ...

# class Recipes(Enum):
#     ...
