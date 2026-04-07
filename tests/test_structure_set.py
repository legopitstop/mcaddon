from mcaddon import StructureSet, __format_version__
from conftest import BedrockSamples


def test_dump_structure_set():
    result = {
        "format_version": __format_version__,
        "minecraft:structure_set": {
            "description": {"identifier": "minecraft:structure_set"},
            "placement": {
                "type": "minecraft:random_spread",
                "salt": 0,
                "separation": 0,
                "spacing": 0,
                "spread_type": "linear",
            },
            "structures": [],
        },
    }
    obj = StructureSet()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_structure_sets(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.bp.glob("*/worldgen/structure_sets/*.json"):
        print(file)
        with StructureSet.open(file) as structure:
            print(structure.id)

            data = structure.model_dump()
            result = StructureSet.model_validate(data)
            assert data == result.model_dump()
