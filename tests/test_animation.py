from mcaddon import Animations, Animation
from conftest import BedrockSamples


def test_dump_animation():
    result = {
        "format_version": "1.10.0",
        "animations": {
            "animations": {
                "animation.test": {
                    "loop": True,
                    "bones": {},
                    "sound_effects": {},
                    "particle_effects": {},
                }
            }
        },
    }
    obj = Animations()
    obj.animations["animation.test"] = Animation(loop=True)
    assert obj.model_dump() == result, obj.model_dump()


def test_open_animations(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.rp.glob("*/animations/*.json"):
        print(file)
        with Animations.open(file) as anim:
            print(anim)
