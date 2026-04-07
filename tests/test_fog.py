from mcaddon import FogSettings, BaseDescription
from conftest import BedrockSamples


def test_dump_fog():
    result = {
        "format_version": "1.16.100",
        "minecraft:fog_settings": {"description": {"identifier": ""}},
    }
    obj = FogSettings(description=BaseDescription(identifier=""))
    assert obj.model_dump() == result, obj.model_dump()


def test_open_fogs(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.rp.glob("*/fogs/*.json"):
        print(file)
        with FogSettings.open(file) as fog:
            print(fog.id)

            data = fog.model_dump()
            result = FogSettings.model_validate(data)
            assert fog == result
