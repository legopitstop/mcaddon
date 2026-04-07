from mcaddon import LocaleText
from conftest import BedrockSamples


def test_open_texts(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.rp.glob("*/texts/*.lang"):
        print(file)
        with LocaleText.open(file) as texts:
            print(texts.translate("gui.ok"))
