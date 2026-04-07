from mcaddon import Attachable, AttachableDescription
from conftest import BedrockSamples


def test_dump_attachable():
    result = {
        "format_version": "1.10.0",
        "minecraft:attachable": {
            "description": {
                "identifier": "",
                "materials": {},
                "textures": {},
                "geometry": {},
                "animations": {},
                "item": {},
                "render_controllers": [],
            }
        },
    }
    obj = Attachable(description=AttachableDescription(identifier=""))
    assert obj.model_dump() == result, obj.model_dump()


def test_open_attachables(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.rp.glob("*/attachables/*.json"):
        print(file)
        with Attachable.open(file) as att:
            print(att.id)

            data = att.model_dump()
            result = Attachable.model_validate(data)
            assert att == result
