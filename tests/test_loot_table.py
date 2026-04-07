from mcaddon import LootTable
from conftest import BedrockSamples


def test_dump_loot_table():
    result = {"pools": [], "type": None}
    obj = LootTable()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_loot_tables(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.bp.glob(
        "*/loot_tables/**/*.json",
    ):
        print(file)
        with LootTable.open(file) as loot:
            print(loot.id)

            data = loot.model_dump()
            result = LootTable.model_validate(data)
            assert data == result.model_dump()
