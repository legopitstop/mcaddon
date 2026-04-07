from mcaddon import TemplatePool, __format_version__
from conftest import BedrockSamples


def test_dump_template_pool():
    result = {
        "format_version": __format_version__,
        "minecraft:template_pool": {
            "description": {"identifier": "minecraft:template_pool"},
            "elements": [],
        },
    }
    obj = TemplatePool()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_template_pools(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.bp.glob("*/worldgen/processors/*.json"):
        print(file)
        with TemplatePool.open(file) as pool:
            print(pool.id)

            data = pool.model_dump()
            result = TemplatePool.model_validate(data)
            assert data == result.model_dump()
