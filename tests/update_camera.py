from mcaddon import CameraPreset

with CameraPreset.load("build/camera.json") as ctx:
    ctx.identifier = "custom:camera"
