from mcaddon import Particle
from conftest import BedrockSamples


def test_dump_particle():
    result = {
        "format_version": "1.10.0",
        "particle_effect": {
            "description": {
                "identifier": "minecraft:explosion_emitter",
                "basic_render_parameters": {
                    "material": "particle",
                    "texture": "textures/particle/explosion",
                },
            },
            "components": {},
            "events": {},
            "curves": {},
        },
    }
    obj = Particle()
    print(obj.model_dump())
    assert obj.model_dump() == result, obj.model_dump()


def test_open_particles(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.rp.glob("*/particles/*.json"):
        print(file)
        with Particle.open(file) as effect:
            print(effect.id)

            data = effect.model_dump()
            result = Particle.model_validate(data)
            assert data == result.model_dump()
