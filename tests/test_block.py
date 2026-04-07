from mcaddon import Block, __format_version__
from conftest import BedrockSamples


def test_dump_block():
    result = {
        "format_version": __format_version__,
        "minecraft:block": {
            "description": {"identifier": "minecraft:air", "states": {}, "traits": {}},
            "components": {},
            "permutations": [],
        },
    }
    obj = Block()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_blocks(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.bp.glob("*/blocks/**/*.json"):
        print(file)
        with Block.open(file) as block:
            print(block.id)

            data = block.model_dump()
            result = Block.model_validate(data)
            assert data == result.model_dump()
