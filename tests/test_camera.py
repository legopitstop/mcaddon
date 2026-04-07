from mcaddon import Camera, __format_version__
from conftest import BedrockSamples


def test_dump_camera():
    result = {"format_version": __format_version__, "minecraft:camera": {}}
    obj = Camera()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_cameras(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.rp.glob("*/cameras/**/*.json"):
        print(file)
        with Camera.open(file) as camera:
            print(camera.id)

            data = camera.model_dump()
            result = Camera.model_validate(data)
            assert data == result.model_dump()
