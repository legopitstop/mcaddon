from mcaddon import *

class ExampleRP(ResourcePack):
    def __init__(self):
        m = Manifest.resource()
        m.header.name = 'My Pack'
        m.header.description = 'Adds some cool stuff'
        ResourcePack.__init__(self, m)

class ExampleBP(BehaviorPack):
    def __init__(self):
        m = Manifest.behavior()
        m.header.name = 'My Pack'
        m.header.description = 'Adds some cool stuff'
        BehaviorPack.__init__(self, m)

class ExampleAddon(Addon):
    def __init__(self):
        Addon.__init__(self, ExampleRP(), ExampleBP())

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
# root.add_block(SaplingBlock('test:sapling', ['test:tree1', 'test:tree2']))
# root.add_block(CropBlock('test:crop'))
# root.add_block(BushBlock('test:bush'))
# root.add_block(CakeBlock('test:cake'))
# root.add_block(CandleCakeBlock('test:candle_cake'))
# root.add_block(DoorBlock('test:door'))
# root.add_block(TrapdoorBlock('test:trapdoor'))
# root.add_block(ButtonBlock('test:button'))
# root.add_block(PressurePlateBlock('test:pressure_plate'))
# root.add_block(CauldronBlock('test:cauldron'))
# root.add_block(CauldronLevelBlock('test:cauldron_level'))
# root.add_block(FenceBlock('test:fence'))
# root.add_block(FenceGateBlock('test:fence_gate'))
# root.add_block(GlassPane('test:glass_pane'))
# root.add_block(LanternBlock('test:lantern'))
# root.add_block(TorchBlock('test:torch'))
# root.add_block(WallBlock('test:wall'))

root.add_item(AppleItem('test:apple'))

# CUSTOM

# Initilize example block
blk = ExampleBlock('test:block')
root.add_block(blk)

# Initilize example item
itm = ExampleItem('test:item')
root.add_item(itm)

# root.behaviors.save('gen/example_BP.zip')
# root.resources.save('gen/example_RP.zip')
root.save('gen/addon')