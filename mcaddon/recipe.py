from typing import Self

from .item import ItemStack
from .registry import INSTANCE, Registries
from .exception import RecipeTypeNotFoundError
from .constant import RecipeTag
from .file import JsonFile, Loader
from .util import getattr2, Identifier, Identifiable


class Ingredient:
    def __init__(self, item: ItemStack = None, tag: Identifier = None):
        self.item = item
        self.tag = tag

    @property
    def __dict__(self) -> dict:
        data = {}
        if self.item:
            data = self.item.__dict__
        elif self.tag:
            data["tag"] = str(self.tag)
        return data

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
        return getattr(self, "_item")

    @item.setter
    def item(self, value: ItemStack):
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_item", value)

    @property
    def tag(self) -> Identifier:
        """Tag used as input for the recipe."""
        return getattr(self, "_tag")

    @tag.setter
    def tag(self, value: Identifier):
        if not isinstance(value, (Identifier, str)):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_tag", Identifier(value))


class Recipe(JsonFile, Identifiable):
    EXTENSION = ".json"
    FILENAME = "recipe"
    DIRNAME = "recipes"

    def __init__(self, identifier: Identifier | str, tags: list[RecipeTag] = None):
        Identifiable.__init__(self, identifier)
        self.tags = tags

    def __str__(self) -> str:
        return "Recipe{" + str(self.identifier) + "}"

    @property
    def __dict__(self) -> dict:
        recipe = {
            "tags": [
                str(tag._value_) if isinstance(tag, RecipeTag) else str(tag)
                for tag in self.tags
            ]
        }
        data = {
            "format_version": "1.20.51",
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
        raise RecipeTypeNotFoundError(data)

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier(value))

    @property
    def tags(self) -> list[RecipeTag]:
        """Item used in a Recipe."""
        return getattr2(self, "_tags", [])

    @tags.setter
    def tags(self, value: list[RecipeTag]):
        if value is None:
            self.tags = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
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
        setattr(self, "_result", value)

    def add_tag(self, tag: RecipeTag | str) -> str:
        if not isinstance(tag, (RecipeTag, str)):
            raise TypeError(
                f"Expected RecipeTag but got '{tag.__class__.__name__}' instead"
            )
        self.tags.append(tag)
        return tag

    def remove_tag(self, tag: RecipeTag | str) -> Self:
        self.tags.remove(tag)
        return self

    def clear_tags(self) -> Self:
        self.tags = []
        return self


INSTANCE.create_registry(Registries.RECIPE_TYPE, Recipe)


def recipe_type(cls):
    """
    Add this recipe type to the registry
    """

    def wrapper():
        return INSTANCE.register(Registries.RECIPE_TYPE, cls.id, cls)

    return wrapper()


@recipe_type
class FurnaceRecipe(Recipe):
    """Represents a furnace recipe for a furnace.'Input' items will burn and transform into items specified in 'output'."""

    id = Identifier("recipe_furnace")

    def __init__(
        self, identifier: Identifier | str, input: ItemStack, output: ItemStack
    ):
        Recipe.__init__(self, identifier)
        self.input = input
        self.output = output
        self.add_tag(RecipeTag.furnace)

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data[str(self.id)]["input"] = str(self.input.item)
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
        setattr(self, "_output", value)


class FurnaceRecipeLoader(Loader):
    name = "Furnace Recipe"

    def __init__(self):
        from .schemas import FurnaceSchem1

        Loader.__init__(self, FurnaceRecipe)
        self.add_schema(FurnaceSchem1, "1.12")
        self.add_schema(FurnaceSchem1, "1.20.10")
        self.add_schema(FurnaceSchem1, "1.20.51")


@recipe_type
class BrewingContainerRecipe(Recipe):
    """Represents a Potion Brewing Container Recipe."""

    id = Identifier("recipe_brewing_container")

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
        self.add_tag(RecipeTag.brewing_stand)

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        setattr(self, "_output", value)


class BrewingContainerRecipeLoader(Loader):
    name = "Brewing Container Recipe"

    def __init__(self):
        from .schemas import BrewingContainerSchem1

        Loader.__init__(self, BrewingContainerRecipe)
        self.add_schema(BrewingContainerSchem1, "1.12")
        self.add_schema(BrewingContainerSchem1, "1.20.10")


@recipe_type
class BrewingMixRecipe(Recipe):
    """Represents a Potion Brewing Mix."""

    id = Identifier("recipe_brewing_mix")

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
        self.add_tag(RecipeTag.brewing_stand)

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        setattr(self, "_output", value)


class BrewingMixRecipeLoader(Loader):
    name = "Brewing Mix Recipe"

    def __init__(self):
        from .schemas import BrewingMixSchem1

        Loader.__init__(self, BrewingMixRecipe)
        self.add_schema(BrewingMixSchem1, "1.12")
        self.add_schema(BrewingMixSchem1, "1.20.10")


@recipe_type
class ShapedRecipe(Recipe):
    """
    Represents a shaped crafting recipe for a crafting table.

    The key used in the pattern may be any single character except the 'space' character, which is reserved for empty slots in a recipe.
    """

    id = Identifier("recipe_shaped")

    def __init__(self, identifier: Identifier, pattern: list[str], result: ItemStack):
        Recipe.__init__(self, identifier)
        self.pattern = pattern
        self.key = {}
        self.result = result
        self.add_tag(RecipeTag.crafting_table)

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data[str(self.id)]["pattern"] = self.pattern
        data[str(self.id)]["key"] = {}
        for k, v in self.key.items():
            data[str(self.id)]["key"][k] = v.__dict__
        data[str(self.id)]["result"] = self.result.__dict__
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
        self.add_schema(ShapedSchem1, "1.20.51")


@recipe_type
class ShapelessRecipe(Recipe):
    id = Identifier("recipe_shapeless")

    def __init__(self, identifier: Identifier, result: ItemStack):
        Recipe.__init__(self, identifier)
        self.ingredients = []
        self.result = result
        self.add_tag(RecipeTag.crafting_table)

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data[str(self.id)]["ingredients"] = [x.__dict__ for x in self.ingredients]
        data[str(self.id)]["result"] = self.result.__dict__
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = ShapelessRecipeLoader()
        loader.validate(data)
        return loader.load(data)

    @property
    def ingredients(self) -> list[RecipeTag]:
        """items used as input (without a shape) for the recipe."""
        return getattr2(self, "_ingredients", [])

    @ingredients.setter
    def ingredients(self, value: list[RecipeTag]):
        if value is None:
            self.ingredients = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
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
        self.add_schema(ShapelessSchem1, "1.20.51")


@recipe_type
class SmithingTransformRecipe(Recipe):
    """
    Represents a Smithing Transform Recipe for the Smithing Table.

    This recipe transforms an item into another one, while retaining its properties.
    """

    id = Identifier("recipe_smithing_transform")

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
        self.add_tag(RecipeTag.smithing_table)

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
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
        setattr(self, "_result", value)


class SmithingTransformRecipeLoader(Loader):
    name = "Smithing Transform Recipe"

    def __init__(self):
        from .schemas import SmithingTransformSchem1, SmithingTransformSchem2

        Loader.__init__(self, SmithingTransformRecipe)
        self.add_schema(SmithingTransformSchem2, "1.12")
        self.add_schema(SmithingTransformSchem1, "1.20.10")
        self.add_schema(SmithingTransformSchem1, "1.20.51")


@recipe_type
class SmithingTrimRecipe(Recipe):
    """
    Represents a Smithing Trim Recipe for the Smithing Table.

    This recipe applies a colored trim pattern to an item, while preserving its other properties.
    """

    id = Identifier("recipe_smithing_trim")

    def __init__(
        self,
        identifier: Identifier,
        template: ItemStack,
        base: ItemStack,
        addition: ItemStack,
    ):
        Recipe.__init__(self, identifier)
        self.template = template
        self.base = base
        self.addition = addition
        self.add_tag(RecipeTag.smithing_table)

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data[str(self.id)]["template"] = str(self.template.item)
        data[str(self.id)]["base"] = str(self.base.item)
        data[str(self.id)]["addition"] = str(self.addition.item)
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
        setattr(self, "_addition", value)


class SmithingTrimRecipeLoader(Loader):
    name = "Smithing Trim Recipe"

    def __init__(self):
        from .schemas import SmithingTrimSchem1

        Loader.__init__(self, SmithingTrimRecipe)
        self.add_schema(SmithingTrimSchem1, "1.12")
        self.add_schema(SmithingTrimSchem1, "1.20.10")
        self.add_schema(SmithingTrimSchem1, "1.20.51")


@recipe_type
class MaterialReductionRecipe(Recipe):
    id = Identifier("recipe_material_reduction")

    def __init__(
        self, identifier: Identifier, input: ItemStack, output: list[ItemStack]
    ):
        Recipe.__init__(self, identifier)
        self.input = input
        self.output = output
        self.add_tag(RecipeTag.material_reducer)

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data[str(self.id)]["input"] = str(self.input.item)
        data[str(self.id)]["output"] = [str(x.item) for x in self.output]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = MaterialReductionRecipeLoader()
        loader.validate(data)
        return loader.load(data)

    @property
    def input(self) -> ItemStack:
        return getattr(self, "_input")

    @input.setter
    def input(self, value: ItemStack):
        if not isinstance(value, ItemStack):
            raise TypeError(
                f"Expected ItemStack but got '{value.__class__.__name__}' instead"
            )
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
        setattr(self, "_output", value)


class MaterialReductionRecipeLoader(Loader):
    mame = "Material Reduction Recipe"

    def __init__(self):
        from .schemas import MaterialReductionSchem1

        Loader.__init__(self, MaterialReductionRecipe)
        self.add_schema(MaterialReductionSchem1, "1.14")


# SHORTCUT
class StonecuttingRecipe(ShapelessRecipe):
    def __init__(self, identifier: Identifier, result: ItemStack):
        ShapelessRecipe.__init__(self, identifier, result)
        self.clear_tags()
        self.add_tag(RecipeTag.stonecutter)
