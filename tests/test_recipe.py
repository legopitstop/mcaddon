from mcaddon import (
    Recipe,
    FurnaceRecipe,
    BaseDescription,
    PotionBrewingMixRecipe,
    PotionBrewingRecipe,
    ShapedRecipe,
    ShapelessRecipe,
    SmithingTransformRecipe,
    SmithingTrimRecipe,
)
from conftest import BedrockSamples


def test_dump_recipe():
    format_version = "1.20.10"
    result = {
        "format_version": format_version,
        "minecraft:recipe_brewing_container": {
            "description": {"identifier": "minecraft:brewing_container"},
            "input": "",
            "reagent": "",
            "output": "",
            "tags": ["brewing_stand"],
        },
    }
    obj = PotionBrewingRecipe(
        description=BaseDescription(identifier="minecraft:brewing_container"),
        input="",
        reagent="",
        output="",
    )
    assert obj.model_dump() == result, obj.model_dump()

    result = {
        "format_version": format_version,
        "minecraft:recipe_brewing_mix": {
            "description": {"identifier": "minecraft:brewing_mix"},
            "input": "",
            "reagent": "",
            "output": "",
            "tags": ["brewing_stand"],
        },
    }
    obj = PotionBrewingMixRecipe(
        description=BaseDescription(identifier="minecraft:brewing_mix"),
        input="",
        reagent="",
        output="",
    )
    assert obj.model_dump() == result, obj.model_dump()

    result = {
        "format_version": format_version,
        "minecraft:recipe_furnace": {
            "description": {"identifier": "minecraft:beef_furnance"},
            "input": "beef",
            "output": "cooked_beef",
            "tags": ["furnace"],
        },
    }
    obj = FurnaceRecipe(
        description=BaseDescription(identifier="minecraft:beef_furnance"),
        input="beef",
        output="cooked_beef",
    )
    assert obj.model_dump() == result, obj.model_dump()

    result = {
        "format_version": format_version,
        "minecraft:recipe_shaped": {
            "description": {"identifier": "minecraft:shaped"},
            "result": "",
            "pattern": [],
            "key": {},
            "tags": ["crafting_table"],
        },
    }
    obj = ShapedRecipe(
        description=BaseDescription(identifier="minecraft:shaped"), result=""
    )
    assert obj.model_dump() == result, obj.model_dump()

    result = {
        "format_version": format_version,
        "minecraft:recipe_shapeless": {
            "description": {"identifier": "minecraft:shapeless"},
            "result": "",
            "ingredients": [],
            "tags": ["crafting_table"],
        },
    }
    obj = ShapelessRecipe(
        description=BaseDescription(identifier="minecraft:shapeless"), result=""
    )
    assert obj.model_dump() == result, obj.model_dump()

    result = {
        "format_version": format_version,
        "minecraft:recipe_smithing_transform": {
            "description": {"identifier": "minecraft:smithing_transform"},
            "template": "",
            "base": "",
            "addition": "",
            "result": "",
            "tags": ["smithing_table"],
        },
    }
    obj = SmithingTransformRecipe(
        description=BaseDescription(identifier="minecraft:smithing_transform"),
        addition="",
        base="",
        result="",
        template="",
    )
    assert obj.model_dump() == result, obj.model_dump()

    result = {
        "format_version": format_version,
        "minecraft:recipe_smithing_trim": {
            "description": {"identifier": "minecraft:smithing_trim"},
            "template": "",
            "base": "",
            "addition": "",
            "tags": ["smithing_table"],
        },
    }
    obj = SmithingTrimRecipe(
        description=BaseDescription(identifier="minecraft:smithing_trim"),
        addition="",
        base="",
        template="",
    )
    assert obj.model_dump() == result, obj.model_dump()


def test_open_recipes(bedrock_samples: BedrockSamples):
    for file in bedrock_samples.bp.glob("*/recipes/*.json"):
        print(file)
        with Recipe.open(file) as recipe:
            print(recipe.__class__.__name__)
            data = recipe.model_dump()
            result = Recipe.model_validate(data)
            assert data == result.model_dump()
