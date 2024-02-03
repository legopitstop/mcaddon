from mcaddon import *

blk = Block.from_settings("test:block", BlockSettings().strength(10))
blk.save("build/")
