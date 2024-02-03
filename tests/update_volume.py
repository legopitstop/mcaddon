from mcaddon import *

with Volume.load("build/volume.json") as ctx:
    ctx.identifier = "custom:volume"

# vol = Volume.load('build/volume.json')
# print(vol)
