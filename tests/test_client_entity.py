from mcaddon import ClientEntity, ClientEntityDescription
from conftest import BedrockSamples


def test_dump_client_entity():
    result = {
        "format_version": "1.10.0",
        "minecraft:client_entity": {
            "description": {
                "identifier": "",
                "materials": {},
                "textures": {},
                "geometry": {},
                "animations": {},
                "particle_effects": {},
                "sound_effects": {},
                "play_sound": {},
                "render_controllers": [],
                "enable_attachables": False,
                "animation_controllers": [],
                "particle_emitters": {},
            }
        },
    }
    obj = ClientEntity(description=ClientEntityDescription(identifier=""))
    assert obj.model_dump() == result, obj.model_dump()


def test_open_client_entities(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.rp.glob("*/entity/*.json"):
        print(file)
        with ClientEntity.open(file) as entity:
            print(entity.id)

            data = entity.model_dump()
            result = ClientEntity.model_validate(data)
            assert entity == result
