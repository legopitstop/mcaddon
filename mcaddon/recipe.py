from typing import Self

from . import VERSION
from .exception import TypeNotFoundError
from .registry import INSTANCE, Registries

from .item import ItemStack
from .pack import behavior_pack
from .file import JsonFile, Loader, Misc
from .util import (
    getattr2,
    getitem,
    additem,
    removeitem,
    clearitems,
    Identifier,
    Identifiable,
)


class Ingredient(Misc):
    def __init__(self, item: ItemStack = None, tag: Identifiable = None):
        self.item = item
        self.tag = tag

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "item" in data:
            self.item = ItemStack.from_dict(data)
        elif "tag" in data:
            self.tag = data.pop("tag")
        return self

    @property
    def item(self) -> ItemStack:
        """Item used as input for the recipe."""
        return getattr(self, "_item", None)

    @item.setter
    def item(self, value: ItemStack):
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
        self.on_update("item", value)
        setattr(self, "_item", value)

    @property
    def tag(self) -> Identifier:
        """Tag used as input for the recipe."""
        return getattr(self, "_tag", None)

    @tag.setter
    def tag(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("tag", id)
        setattr(self, "_tag", id)

    def jsonify(self) -> dict:
        data = {}
        if self.item:
            data = self.item.jsonify()
        elif self.tag:
            data["tag"] = str(self.tag)
        return data

    @staticmethod
    def of(obj) -> Self:
        if isinstance(obj, Ingredient):
            return obj
        elif isinstance(obj, ItemStack):
            return Ingredient(obj)
        res = str(obj)
        if res.startswith("#"):
            return Ingredient(tag=res.replace("#", "", 1))
        return Ingredient(ItemStack(res))


class Recipe(JsonFile, Identifiable):
    def __init__(self, identifier: Identifiable, tags: list[str] = []):
        Identifiable.__init__(self, identifier)
        self.tags = tags

    def __str__(self) -> str:
        return self.__class__.__name__ + "{" + str(self.identifier) + "}"

    def jsonify(self) -> dict:
        recipe = {"tags": [str(tag) for tag in self.tags]}
        data = {
            "format_version": "1.20.50",
            str(self.id): {"description": {"identifier": str(self.identifier)}},
        }
        for k, v in recipe.items():
            data[str(self.id)][k] = v
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        for k, v in INSTANCE.get_registry(Registries.RECIPE_TYPE).items():
            if str(k) in data:
                self = v.from_dict(data)
                dat = data.get(str(self.id))
                self.identifier = dat["description"]["identifier"]
                return self
        raise TypeNotFoundError(data)

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier.of(value))

    @property
    def tags(self) -> list[str]:
        """Item used in a Recipe."""
        return getattr2(self, "_tags", [])

    @tags.setter
    def tags(self, value: list[str]):
        if value is None:
            self.tags = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("tags", value)
        setattr(self, "_tags", value)

    @property
    def result(self) -> ItemStack | list[ItemStack]:
        """Item(s) used as output for the recipe."""
        return getattr(self, "_result")

    @result.setter
    def result(self, value: ItemStack | list[ItemStack]):
        if isinstance(value, list):
            setattr(self, "_result", value)
            return
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
        self.on_update("result", value)
        setattr(self, "_result", value)

    def get_tag(self, index: int) -> str:
        return getitem(self, "tags", index)

    def add_tag(self, tag: str | str) -> str:
        return additem(self, "tags", tag, type=str)

    def remove_tag(self, index: int) -> Self:
        return removeitem(self, "tags", index)

    def clear_tags(self) -> Self:
        """Remove all tags"""
        return clearitems(self, "tags")


INSTANCE.create_registry(Registries.RECIPE_TYPE, Recipe)


def recipe_type(cls):
    """
    Add this recipe type to the registry
    """

    def wrapper():
        return INSTANCE.register(Registries.RECIPE_TYPE, cls.id, cls)

    return wrapper()


@recipe_type
@behavior_pack
class FurnaceRecipe(Recipe):
    """Represents a [furnace recipe](https://bedrock.dev/docs/stable/Recipes#Furnace%20Recipe) for a furnace.'Input' items will burn and transform into items specified in 'output'."""

    id = Identifier("recipe_furnace")
    FILEPATH = "recipes/recipe_furnace.json"

    def __init__(
        self, identifier: Identifier | str, input: Ingredient, output: ItemStack
    ):
        Recipe.__init__(self, identifier)
        self.input = input
        self.output = output
        self.add_tag("furnace")

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["input"] = self.input.item.jsonify()
        data[str(self.id)]["output"] = str(self.output.item)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = FurnaceRecipeLoader()
        loader.validate(data)
        return loader.load(data)

    @property
    def input(self) -> Ingredient:
        """Items used as input for the furnace recipe."""
        return getattr(self, "_input")

    @input.setter
    def input(self, value: Ingredient):
        if not isinstance(value, Ingredient):
            raise TypeError(
                f"Expected Ingredient but got '{value.__class__.__name__}' instead"
            )
        self.on_update("input", value)
        setattr(self, "_input", value)

    @property
    def output(self) -> ItemStack:
        """Items used as output for the furnace recipe."""
        return getattr(self, "_output")

    @output.setter
    def output(self, value: ItemStack):
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
        self.on_update("output", value)
        setattr(self, "_output", value)


class FurnaceRecipeLoader(Loader):
    name = "Furnace Recipe"

    def __init__(self):
        from .schemas import FurnaceSchem1

        Loader.__init__(self, FurnaceRecipe)
        self.add_schema(FurnaceSchem1, "1.12")
        self.add_schema(FurnaceSchem1, "1.20.10")
        self.add_schema(FurnaceSchem1, "1.20.50")


@recipe_type
@behavior_pack
class BrewingContainerRecipe(Recipe):
    """Represents a [Potion Brewing Container Recipe](https://bedrock.dev/docs/stable/Recipes#Potion%20Brewing%20Container%20Recipe)."""

    id = Identifier("recipe_brewing_container")
    FILEPATH = "recipes/recipe_brewing_container.json"

    def __init__(
        self,
        identifier: Identifier,
        input: ItemStack,
        reagent: ItemStack,
        output: ItemStack,
    ):
        Recipe.__init__(self, identifier)
        self.input = input
        self.reagent = reagent
        self.output = output
        self.add_tag("brewing_stand")

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["input"] = str(self.input.item)
        data[str(self.id)]["reagent"] = str(self.reagent.item)
        data[str(self.id)]["output"] = str(self.output.item)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = BrewingContainerRecipeLoader()
        loader.validate(data)
        return loader.load(data)

    @property
    def input(self) -> ItemStack:
        """input potion used in the brewing container recipe."""
        return getattr(self, "_input")

    @input.setter
    def input(self, value: ItemStack):
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
        self.on_update("input", value)
        setattr(self, "_input", value)

    @property
    def reagent(self) -> ItemStack:
        """item used in the brewing container recipe with the input potion."""
        return getattr(self, "_reagent")

    @reagent.setter
    def reagent(self, value: ItemStack):
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
        self.on_update("reagent", value)
        setattr(self, "_reagent", value)

    @property
    def output(self) -> ItemStack:
        """output potion from the brewing container recipe."""
        return getattr(self, "_output")

    @output.setter
    def output(self, value: ItemStack):
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
        self.on_update("output", value)
        setattr(self, "_output", value)


class BrewingContainerRecipeLoader(Loader):
    name = "Brewing Container Recipe"

    def __init__(self):
        from .schemas import BrewingContainerSchem1

        Loader.__init__(self, BrewingContainerRecipe)
        self.add_schema(BrewingContainerSchem1, "1.12")
        self.add_schema(BrewingContainerSchem1, "1.20.10")
        self.add_schema(BrewingContainerSchem1, "1.20.50")


@recipe_type
@behavior_pack
class BrewingMixRecipe(Recipe):
    """Represents a [Potion Brewing Mix](https://bedrock.dev/docs/stable/Recipes#Potion%20Brewing%20Mix)."""

    id = Identifier("recipe_brewing_mix")
    FILEPATH = "recipes/recipe_brewing_mix.json"

    def __init__(
        self,
        identifier: Identifier,
        input: ItemStack,
        reagent: ItemStack,
        output: ItemStack,
    ):
        Recipe.__init__(self, identifier)
        self.input = input
        self.reagent = reagent
        self.output = output
        self.add_tag("brewing_stand")

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["input"] = str(self.input.item)
        data[str(self.id)]["reagent"] = str(self.reagent.item)
        data[str(self.id)]["output"] = str(self.output.item)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = BrewingMixRecipeLoader()
        loader.validate(data)
        return loader.load(data)

    @property
    def input(self) -> ItemStack:
        """input potion used on the brewing stand."""
        return getattr(self, "_input")

    @input.setter
    def input(self, value: ItemStack):
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
        self.on_update("input", value)
        setattr(self, "_input", value)

    @property
    def reagent(self) -> ItemStack:
        """item used to mix with the input potion."""
        return getattr(self, "_reagent")

    @reagent.setter
    def reagent(self, value: ItemStack):
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
        self.on_update("reagent", value)
        setattr(self, "_reagent", value)

    @property
    def output(self) -> ItemStack:
        """output potion from mixing the input potion with the reagent on the brewing stand."""
        return getattr(self, "_output")

    @output.setter
    def output(self, value: ItemStack):
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
        self.on_update("output", value)
        setattr(self, "_output", value)


class BrewingMixRecipeLoader(Loader):
    name = "Brewing Mix Recipe"

    def __init__(self):
        from .schemas import BrewingMixSchem1

        Loader.__init__(self, BrewingMixRecipe)
        self.add_schema(BrewingMixSchem1, "1.12")
        self.add_schema(BrewingMixSchem1, "1.20.10")
        self.add_schema(BrewingMixSchem1, "1.20.50")


@recipe_type
@behavior_pack
class ShapedRecipe(Recipe):
    """
    Represents a [shaped crafting recipe](https://bedrock.dev/docs/stable/Recipes#Shaped%20Recipe) for a crafting table.

    The key used in the pattern may be any single character except the 'space' character, which is reserved for empty slots in a recipe.
    """

    id = Identifier("recipe_shaped")
    FILEPATH = "recipes/recipe_shaped.json"

    def __init__(
        self, identifier: Identifier, result: ItemStack, pattern: list[str] = []
    ):
        Recipe.__init__(self, identifier)
        self.pattern = pattern
        self.key = {}
        self.result = result
        self.add_tag("crafting_table")

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["pattern"] = self.pattern
        data[str(self.id)]["key"] = {}
        for k, v in self.key.items():
            data[str(self.id)]["key"][k] = v.jsonify()

        if isinstance(self.result, list):
            data[str(self.id)]["result"] = [x.jsonify() for x in self.result]
        else:
            data[str(self.id)]["result"] = self.result.jsonify()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = ShapedRecipeLoader()
        loader.validate(data)
        return loader.load(data)

    @property
    def pattern(self) -> list[str]:
        """characters that represent a pattern to be defined by keys."""
        return getattr2(self, "_pattern", [])

    @pattern.setter
    def pattern(self, value: list[str]):
        if value is None:
            self.pattern = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("pattern", value)
        setattr(self, "_pattern", value)

    @property
    def key(self) -> dict[str, ItemStack]:
        """patten key character mapped to item names."""
        return getattr2(self, "_key", {})

    @key.setter
    def key(self, value: dict[str, ItemStack]):
        if value is None:
            self.key = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        self.on_update("key", value)
        setattr(self, "_key", value)

    def add_key(self, key: str, stack: ItemStack) -> ItemStack:
        if not isinstance(stack, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{stack.__class__.__name__}' instead"
            )
        self.key[key] = stack
        return stack

    def remove_key(self, key: str) -> ItemStack:
        return self.key.pop(key)

    def clear_keys(self) -> Self:
        self.key = {}
        return self


class ShapedRecipeLoader(Loader):
    """Represents a shapeless crafting recipe."""

    name = "Shaped Recipe"

    def __init__(self):
        from .schemas import ShapedSchem1

        Loader.__init__(self, ShapedRecipe)
        self.add_schema(ShapedSchem1, "1.12")
        self.add_schema(ShapedSchem1, "1.14")
        self.add_schema(ShapedSchem1, "1.16")
        self.add_schema(ShapedSchem1, "1.20.10")
        self.add_schema(ShapedSchem1, "1.20.50")


@recipe_type
@behavior_pack
class ShapelessRecipe(Recipe):
    """
    Represents a [shapeless crafting recipe](https://bedrock.dev/docs/stable/Recipes#Shapeless%20Recipe).
    """

    id = Identifier("recipe_shapeless")
    FILEPATH = "recipes/recipe_shapeless.json"

    def __init__(self, identifier: Identifier, result: ItemStack):
        Recipe.__init__(self, identifier)
        self.ingredients = []
        self.result = result
        self.add_tag("crafting_table")

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["ingredients"] = [x.jsonify() for x in self.ingredients]
        data[str(self.id)]["result"] = self.result.jsonify()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = ShapelessRecipeLoader()
        loader.validate(data)
        return loader.load(data)

    @property
    def ingredients(self) -> list[str]:
        """items used as input (without a shape) for the recipe."""
        return getattr2(self, "_ingredients", [])

    @ingredients.setter
    def ingredients(self, value: list[str]):
        if value is None:
            self.ingredients = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("ingredients", value)
        setattr(self, "_ingredients", value)

    def add_ingredient(self, stack: ItemStack) -> ItemStack:
        self.ingredients.append(stack)
        return stack

    def remove_ingredient(self, stack: ItemStack) -> Self:
        self.ingredients.remove(stack)
        return self

    def clear_ingredients(self) -> Self:
        self.ingredients = []
        return self


class ShapelessRecipeLoader(Loader):
    name = "Shapeless Recipe"

    def __init__(self):
        from .schemas import ShapelessSchem1

        Loader.__init__(self, ShapelessRecipe)
        self.add_schema(ShapelessSchem1, "1.12")
        self.add_schema(ShapelessSchem1, "1.16")
        self.add_schema(ShapelessSchem1, "1.19")
        self.add_schema(ShapelessSchem1, "1.20.10")
        self.add_schema(ShapelessSchem1, "1.20.50")


@recipe_type
@behavior_pack
class SmithingTransformRecipe(Recipe):
    """
    Represents a [Smithing Transform Recipe](https://bedrock.dev/docs/stable/Recipes#Smithing%20Transform%20Recipe) for the Smithing Table.

    This recipe transforms an item into another one, while retaining its properties.
    """

    id = Identifier("recipe_smithing_transform")
    FILEPATH = "recipes/recipe_smithing_transform.json"

    def __init__(
        self,
        identifier: Identifier,
        template: ItemStack,
        base: ItemStack,
        addition: ItemStack,
        result: ItemStack,
    ):
        Recipe.__init__(self, identifier)
        self.template = template
        self.base = base
        self.addition = addition
        self.result = result
        self.add_tag("smithing_table")

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["template"] = str(self.template.item)
        data[str(self.id)]["base"] = str(self.base.item)
        data[str(self.id)]["addition"] = str(self.addition.item)
        data[str(self.id)]["result"] = str(self.result.item)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = SmithingTransformRecipeLoader()
        loader.validate(data)
        return loader.load(data)

    @property
    def template(self) -> ItemStack:
        """The template needed to perform the transform operation. In case of stackable items, only 1 item is consumed. Items must have the "minecraft:transform_templates" tag to be accepted into the respective UI slot."""
        return getattr(self, "_template")

    @template.setter
    def template(self, value: ItemStack):
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
        self.on_update("template", value)
        setattr(self, "_template", value)

    @property
    def addition(self) -> ItemStack:
        """The material needed to perform the transform operation. In case of stackable items, only 1 item is consumed. The only accepted item is "minecraft:netherite_ingot". Items must have the "minecraft:transform_materials" tag to be accepted into the respective UI slot."""
        return getattr(self, "_addition")

    @addition.setter
    def addition(self, value: ItemStack):
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
        self.on_update("addition", value)
        setattr(self, "_addition", value)

    @property
    def base(self) -> ItemStack:
        """The item to transform. Its properties will be copied to "result". The only accepted items are armor and tools. Items must have the "minecraft:transformable_items" tag to be accepted into the respective UI slot."""
        return getattr(self, "_base")

    @base.setter
    def base(self, value: ItemStack):
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
        self.on_update("base", value)
        setattr(self, "_base", value)

    @property
    def result(self) -> ItemStack:
        return getattr(self, "_result")

    @result.setter
    def result(self, value: ItemStack):
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
        self.on_update("result", value)
        setattr(self, "_result", value)


class SmithingTransformRecipeLoader(Loader):
    name = "Smithing Transform Recipe"

    def __init__(self):
        from .schemas import SmithingTransformSchem1, SmithingTransformSchem2

        Loader.__init__(self, SmithingTransformRecipe)
        self.add_schema(SmithingTransformSchem2, "1.12")
        self.add_schema(SmithingTransformSchem1, "1.20.10")
        self.add_schema(SmithingTransformSchem1, "1.20.50")


@recipe_type
@behavior_pack
class SmithingTrimRecipe(Recipe):
    """
    Represents a [Smithing Trim Recipe](https://bedrock.dev/docs/stable/Recipes#Smithing%20Trim%20Recipe) for the Smithing Table.

    This recipe applies a colored trim pattern to an item, while preserving its other properties.
    """

    id = Identifier("recipe_smithing_trim")
    FILEPATH = "recipes/recipe_smithing_trim.json"

    def __init__(
        self,
        identifier: Identifier,
        template: Ingredient,
        base: Ingredient,
        addition: Ingredient,
    ):
        Recipe.__init__(self, identifier)
        self.template = template
        self.base = base
        self.addition = addition
        self.add_tag("smithing_table")

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["template"] = self.template.item.jsonify()
        data[str(self.id)]["base"] = self.base.item.jsonify()
        data[str(self.id)]["addition"] = self.addition.item.jsonify()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = SmithingTrimRecipeLoader()
        loader.validate(data)
        return loader.load(data)

    @property
    def template(self) -> Ingredient:
        """The template needed to perform the trim operation. It defines the pattern which will be applied to the item. In case of stackable items, only 1 item is consumed. Items must have the "minecraft:trim_templates" tag to be accepted into the respective UI slot."""
        return getattr(self, "_template")

    @template.setter
    def template(self, value: Ingredient):
        if not isinstance(value, Ingredient):
            raise TypeError(
                f"Expected Ingredient but got '{value.__class__.__name__}' instead"
            )
        self.on_update("template", value)
        setattr(self, "_template", value)

    @property
    def base(self) -> Ingredient:
        """The item to trim. Its properties will be preserved. The only accepted items are armors. Items must have the "minecraft:trimmable_armors" tag to be accepted into the respective UI slot."""
        return getattr(self, "_base")

    @base.setter
    def base(self, value: Ingredient):
        if not isinstance(value, Ingredient):
            raise TypeError(
                f"Expected Ingredient but got '{value.__class__.__name__}' instead"
            )
        self.on_update("base", value)
        setattr(self, "_base", value)

    @property
    def addition(self) -> Ingredient:
        """The material needed to perform the trim operation. It defines the color in which the pattern will be applied to the item. In case of stackable items, only 1 item is consumed. Items must have the "minecraft:trim_materials" tag to be accepted into the respective UI slot."""
        return getattr(self, "_addition")

    @addition.setter
    def addition(self, value: Ingredient):
        if not isinstance(value, Ingredient):
            raise TypeError(
                f"Expected Ingredient but got '{value.__class__.__name__}' instead"
            )
        self.on_update("addition", value)
        setattr(self, "_addition", value)


class SmithingTrimRecipeLoader(Loader):
    name = "Smithing Trim Recipe"

    def __init__(self):
        from .schemas import SmithingTrimSchem1

        Loader.__init__(self, SmithingTrimRecipe)
        self.add_schema(SmithingTrimSchem1, "1.12")
        self.add_schema(SmithingTrimSchem1, "1.20.10")
        self.add_schema(SmithingTrimSchem1, "1.20.50")


@recipe_type
@behavior_pack
class MaterialReductionRecipe(Recipe):
    """
    Represents a Material Reduction Recipe for the Material Reducer.
    """

    id = Identifier("recipe_material_reduction")
    FILEPATH = "recipes/recipe_material_reduction.json"

    def __init__(
        self, identifier: Identifier, input: Ingredient, output: list[ItemStack]
    ):
        Recipe.__init__(self, identifier)
        self.input = input
        self.output = output
        self.add_tag("material_reducer")

    def jsonify(self) -> dict:
        data = super().jsonify()
        data[str(self.id)]["input"] = str(self.input.item)
        data[str(self.id)]["output"] = [x.item.jsonify() for x in self.output]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = MaterialReductionRecipeLoader()
        loader.validate(data)
        return loader.load(data)

    @property
    def input(self) -> Ingredient:
        return getattr(self, "_input")

    @input.setter
    def input(self, value: Ingredient):
        if not isinstance(value, Ingredient):
            raise TypeError(
                f"Expected Ingredient but got '{value.__class__.__name__}' instead"
            )
        self.on_update("input", value)
        setattr(self, "_input", value)

    @property
    def output(self) -> list[ItemStack]:
        return getattr(self, "_output")

    @output.setter
    def output(self, value: list[ItemStack]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("output", value)
        setattr(self, "_output", value)


class MaterialReductionRecipeLoader(Loader):
    mame = "Material Reduction Recipe"

    def __init__(self):
        from .schemas import MaterialReductionSchem1

        Loader.__init__(self, MaterialReductionRecipe)
        self.add_schema(MaterialReductionSchem1, "1.14")


# SHORTCUT


class StonecuttingRecipe(ShapelessRecipe):
    """
    Represents a Shapeless Recipe for the Stonecutter.
    """

    def __init__(self, identifier: Identifier, result: ItemStack):
        ShapelessRecipe.__init__(self, identifier, result)
        self.clear_tags()
        self.add_tag("stonecutter")
