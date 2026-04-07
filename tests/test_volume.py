from mcaddon import Volume, __format_version__
from conftest import BedrockSamples


def test_dump_volume():
    result = {"format_version": __format_version__, "minecraft:volume": {}}
    obj = Volume()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_volumes(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.rp.glob(
        "*/volumes/**/*.json",
    ):
        print(file)
        with Volume.open(file) as volume:
            print(volume.id)

            data = volume.model_dump()
            result = Volume.model_validate(data)
            assert data == result.model_dump()
