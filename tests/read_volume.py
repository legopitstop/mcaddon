from mcaddon import Volume

vol = Volume.load("build/volume.json")
print(vol.identifier)
vol.save("build/output.json")
