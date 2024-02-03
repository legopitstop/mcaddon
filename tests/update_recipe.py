from mcaddon import *

with Recipe.load("build/brewing_container.json") as ctx:
    ctx.identifier = "custom:brewing_container"

with Recipe.load("build/brewing_mix.json") as ctx:
    ctx.identifier = "custom:brewing_mix"

with Recipe.load("build/furnace.json") as ctx:
    ctx.identifier = "custom:furnace"

with Recipe.load("build/shaped.json") as ctx:
    ctx.identifier = "custom:shaped"

with Recipe.load("build/shapeless.json") as ctx:
    ctx.identifier = "custom:shapeless"

with Recipe.load("build/smithing_transform.json") as ctx:
    ctx.identifier = "custom:smithing_transform"

with Recipe.load("build/smithing_trim.json") as ctx:
    ctx.identifier = "custom:smithing_trim"
