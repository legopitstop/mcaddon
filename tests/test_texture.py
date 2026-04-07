from mcaddon import TextureFile
from conftest import BedrockSamples


def test_open_textures(bedrock_samples: BedrockSamples):
    png = bedrock_samples.rp.glob("*/textures/*.png")
    jpg = bedrock_samples.rp.glob("*/textures/*.jpg")
    jpeg = bedrock_samples.rp.glob("*/textures/*.jpeg")
    tga = bedrock_samples.rp.glob("*/textures/*.tga")
    for file in [*png, *jpg, *jpeg, *tga]:
        with TextureFile.open(file) as tex:
            print(tex.id)
