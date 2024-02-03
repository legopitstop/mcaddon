from mcaddon import *

with Item.load("build/item.json") as ctx:
    ctx.identifier = "custom:item"
