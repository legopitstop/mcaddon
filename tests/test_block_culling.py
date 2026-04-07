from mcaddon import BlockCulling, __format_version__
from conftest import BedrockSamples


def test_dump_block_culling():
    result = {
        "format_version": __format_version__,
        "minecraft:block_culling_rules": {
            "description": {
                "identifier": "minecraft:test",
            },
            "rules": [],
        },
    }
    obj = BlockCulling()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_block_cullings(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.bp.glob("*/block_culling/*.json"):
        print(file)
        with BlockCulling.open(file) as culling:
            print(culling.id)

            data = culling.model_dump()
            result = BlockCulling.model_validate(data)
            assert data == result.model_dump()
