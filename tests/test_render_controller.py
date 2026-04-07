from mcaddon import RenderControllers, RenderController
from conftest import BedrockSamples


def test_dump_render_controller():
    result = {
        "format_version": "1.10.0",
        "render_controllers": {
            "render_controllers": {
                "controller.render.test": {
                    "geometry": "geometry.default",
                    "materials": [{"*": "material.default"}],
                    "textures": ["texture.default"],
                    "part_visibility": [],
                }
            }
        },
    }
    obj = RenderControllers()
    obj.render_controllers["controller.render.test"] = RenderController()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_render_controllers(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.rp.glob("*/render_controllers/*.json"):
        print(file)
        with RenderControllers.open(file) as controller:
            print(controller)
