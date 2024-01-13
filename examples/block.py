from mcaddon import *

blk = Block('test:on_interact_change_state_block')
blk.add_component(OnInteractComponent(event='test_event'))
blk.add_event('test_event', SetBlockState({'custom:direction': "1"}))
blk.save('gen/block.json')