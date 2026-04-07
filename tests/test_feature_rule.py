from mcaddon import FeatureRule, __format_version__
from conftest import BedrockSamples


def test_dump_feature_rule():
    result = {"format_version": __format_version__, "minecraft:feature_rule": {}}
    obj = FeatureRule()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_feature_rules(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.bp.glob("*/feature_rules/*.json"):
        print(file)
        with FeatureRule.open(file) as rule:
            print(rule)

            data = rule.model_dump()
            result = FeatureRule.model_validate(data)
            assert rule == result
