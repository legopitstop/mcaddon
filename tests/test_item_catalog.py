from mcaddon import CraftingItemsCatalog
from conftest import BedrockSamples


def test_dump_item_catalog():
    result = {
        "format_version": "1.21.60",
        "minecraft:crafting_items_catalog": {"categories": []},
    }
    obj = CraftingItemsCatalog()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_item_catalogs(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.bp.glob("*/item_catalog/*.json"):
        print(file)
        with CraftingItemsCatalog.open(file) as catalog:

            data = catalog.model_dump()
            result = CraftingItemsCatalog.model_validate(data)
            assert catalog == result
