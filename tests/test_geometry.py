from mcaddon import Geometries
from conftest import BedrockSamples


def test_open_geometry(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.rp.glob("*/models/entity/*.json"):
        print(file)
        with Geometries.open(file) as anim:
            print(anim)
