from mcaddon import *

itm = Item.from_settings("test:item", ItemSettings().set_count(16))
itm.save("build/")
