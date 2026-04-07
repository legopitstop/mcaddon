import pytest

from mcaddon import BehaviorPack, ResourcePack
from conftest import BedrockSamples


@pytest.fixture
def setup_data():
    # TODO: Download Mojang/bedrock-samples
    ...


def test_open_resource_pack(bedrock_samples: BedrockSamples):
    with ResourcePack.open(bedrock_samples.rp / "vanilla") as rp:
        ...


def test_open_behavior_pack(bedrock_samples: BedrockSamples):
    with BehaviorPack.open(bedrock_samples.bp / "vanilla") as bp:
        ...


# def test_skin_pack():
#     with SkinPack.open() as sp:
#         ...
