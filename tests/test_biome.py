from mcaddon import Biome, BiomeClimateComponent, __format_version__
from conftest import BedrockSamples


def test_dump_biome():
    result = {
        "format_version": __format_version__,
        "minecraft:biome": {
            "description": {"identifier": "minecraft:plains"},
            "components": {"minecraft:climate": {}},
        },
    }
    obj = Biome()
    obj.components.add(BiomeClimateComponent())
    assert obj.model_dump() == result, obj.model_dump()


def test_open_biomes(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.bp.glob("*/biomes/*.json"):
        print(file)
        with Biome.open(file) as biome:
            print(biome.id)

            data = biome.model_dump()
            result = Biome.model_validate(data)
            assert data == result.model_dump()
