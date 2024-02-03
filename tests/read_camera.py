from mcaddon import CameraPreset

blk = CameraPreset.load("build/camera.json")
print(blk.identifier)
blk.save("build/output.json")
