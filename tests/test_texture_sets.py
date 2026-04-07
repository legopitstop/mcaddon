from mcaddon import TextureSet, __format_version__
from conftest import BedrockSamples


def test_dump_texture_set():
    result = {
        "format_version": __format_version__,
        "minecraft:texture_set": {"color": "red"},
    }
    obj = TextureSet(color="red")
    assert obj.model_dump() == result, obj.model_dump()


def test_open_texture_sets(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.rp.glob(
        "*/textures/**/*.texture_set.json",
    ):
        print(file)
        with TextureSet.open(file) as tex:
            print(tex.id)

            data = tex.model_dump()
            result = TextureSet.model_validate(data)
            assert tex == result
