from mcaddon import Block

blk = Block.load("build/block.json")
print(blk.identifier)
blk.save("build/output.json")
