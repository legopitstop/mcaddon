from mcaddon import *

class ExampleAddon(Addon):
    def __init__(self):
        Addon.__init__(self)

# Define example block
class ExampleBlock(Block):
    def __init__(self, id):
        Block.__init__(self, id)
        self.add_component(OnInteractComponent('test_event'))
        self.add_event('test_event', SetBlockState({'custom:direction': "1"}))

        perm = BlockPermutation("asd")
        perm.add_component(TransformationComponent(rotation=[0, 90, 0]))
        self.add_permutation(perm)

# Define example item
class ExampleItem(Item):
    def __init__(self, id):
        Item.__init__(self, id)
        self.add_component(FuelComponent(12.0))
        self.add_component(MaxStackSizeComponent(64))
        self.add_component(IconComponent('blaze_rod'))
        self.add_component(HandEquippedComponent(True))
        self.add_component(DisplayNameComponent('Blaze Rod'))

# Initilize addon
root = ExampleAddon()

# ASSETS+
root.add_block(StairsBlock('test:stairs'))
root.add_block(SlabBlock('test:slab'))
root.add_item(AppleItem('test:apple'))

# CUSTOM

# Initilize example block
blk = ExampleBlock('test:block')
root.add_block(blk)

# Initilize example item
itm = ExampleItem('test:item')
root.add_item(itm)

root.save_folder('gen/addon.mcaddon')