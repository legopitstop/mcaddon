from mcaddon import ProcessorList, __format_version__
from conftest import BedrockSamples


def test_dump_processor():
    result = {
        "format_version": __format_version__,
        "minecraft:processor_list": {
            "description": {"identifier": "minecraft:processor"},
            "processors": [],
        },
    }
    obj = ProcessorList()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_processors(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.bp.glob("*/worldgen/processors/*.json"):
        print(file)
        with ProcessorList.open(file) as processor:
            print(processor.id)

            data = processor.model_dump()
            result = ProcessorList.model_validate(data)
            assert data == result.model_dump()
