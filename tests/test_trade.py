from mcaddon import Trading
from conftest import BedrockSamples


def test_dump_trade():
    result = {"tiers": []}
    obj = Trading()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_trades(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.bp.glob(
        "*/trading/**/*.json",
    ):
        print(file)
        with Trading.open(file) as trade:
            print(trade.id)

            data = trade.model_dump()
            result = Trading.model_validate(data)
            assert data == result.model_dump()
