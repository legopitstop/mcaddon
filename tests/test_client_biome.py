from mcaddon import ClientBiome, __format_version__
from conftest import BedrockSamples


def test_dump_client_biome():
    result = {
        "format_version": __format_version__,
        "minecraft:client_biome": {
            "description": {"identifier": "minecraft:plains"},
            "components": {},
        },
    }
    obj = ClientBiome()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_client_biomes(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.rp.glob("*/biomes/*.json"):
        print(file)
        with ClientBiome.open(file) as biome:
            print(biome.id)

            data = biome.model_dump()
            result = ClientBiome.model_validate(data)
            assert data == result.model_dump()
