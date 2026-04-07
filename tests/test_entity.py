from mcaddon import Entity
from conftest import BedrockSamples


def test_dump_entity():
    result = {
        "format_version": "1.21.50",
        "minecraft:entity": {
            "component_groups": {},
            "components": {},
            "description": {
                "animations": {},
                "identifier": "minecraft:creeper",
                "properties": {},
            },
        },
    }
    obj = Entity()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_entities(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.bp.glob("*/entities/*.json"):
        print(file)
        with Entity.open(file) as item:
            print(item.id)

            data = item.model_dump()
            result = Entity.model_validate(data)
            assert data == result.model_dump()
