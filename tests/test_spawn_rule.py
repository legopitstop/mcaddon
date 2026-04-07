from mcaddon import SpawnRule
from conftest import BedrockSamples


def test_dump_spawn_rule():
    result = {
        "format_version": "1.17.0",
        "minecraft:spawn_rules": {
            "conditions": [],
            "description": {
                "identifier": "minecraft:default_spawn_rules",
                "population_control": "monster",
            },
            "events": {},
        },
    }
    obj = SpawnRule()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_spawn_rules(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.bp.glob("*/spawn_rules/*.json"):
        print(file)
        with SpawnRule.open(file) as rule:
            print(rule.id)

            data = rule.model_dump()
            result = SpawnRule.model_validate(data)
            assert data == result.model_dump()
