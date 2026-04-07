from mcaddon import AnimationControllers, AnimationController, AnimationState
from conftest import BedrockSamples


def test_dump_animation_controller():
    result = {
        "format_version": "1.10.0",
        "animation_controllers": {
            "animation_controllers": {
                "animation.controller.test": {
                    "initial_state": "default",
                    "states": {
                        "default": {
                            "animations": ["idle"],
                            "transitions": [],
                            "particle_effects": [],
                            "sound_effects": [],
                        }
                    },
                }
            }
        },
    }
    obj = AnimationControllers()
    ac = AnimationController()
    ac.states["default"] = AnimationState(animations=["idle"])
    obj.animation_controllers["animation.controller.test"] = ac

    assert obj.model_dump() == result, obj.model_dump()


def test_open_animation_controllers(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.rp.glob("*/animation_controllers/*.json"):
        print(file)
        with AnimationControllers.open(file) as anim:
            print(anim)
