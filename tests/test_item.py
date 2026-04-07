from mcaddon import Item, __format_version__
from conftest import BedrockSamples


def test_dump_item():
    result = {
        "format_version": __format_version__,
        "minecraft:item": {
            "components": {},
            "description": {"identifier": "minecraft:air"},
        },
    }
    obj = Item()
    assert obj.model_dump() == result, obj.model_dump()


def test_parse_items(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.bp.glob("*/items/*.json"):
        print(file)
        with Item.open(file) as item:
            print(item.id)

            data = item.model_dump()
            result = Item.model_validate(data)
            assert data == result.model_dump()
