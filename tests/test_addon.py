from mcaddon import *

from .test_block_culling import blkcull
from .test_block import blk
from .test_camera import cam
from .test_feature_rule import rule
from .test_feature import features
from .test_geometry import geo
from .test_item import itm
from .test_loot import loot1, loot2
from .test_recipe import recipes
from .test_trading import trde
from .test_volume import vol

addon = Addon()

# Add files

addon.add(blk)
addon.add(cam)
addon.add(rule)
for f in features:
    addon.add(f)
addon.add(geo)
addon.add(itm)
addon.add(loot1)
addon.add(loot2)
for r in recipes:
    addon.add(r)
addon.add(trde)
addon.add(vol)
addon.add(blkcull)

addon.save("build/addon", zipped=False, overwrite=True)
