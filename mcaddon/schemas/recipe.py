import os

from .. import __file__, Schema, ItemStack, Ingredient, FurnaceRecipe


class RecipeSchem1(Schema):
    def load(cls, self, data: dict):
        self.identifier = data["description"]["identifier"]


class FurnaceSchem1(RecipeSchem1):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__), "data", "schemas", "recipe", "furnace1.json"
            ),
        )

    def load(cls, self: FurnaceRecipe, data: dict):
        super().load(self, data)
        self.input = Ingredient.from_dict(data.pop("input"))
        self.output = ItemStack.from_dict(data.pop("output"))


class BrewingContainerSchem1(RecipeSchem1):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "recipe",
                "brewing_container1.json",
            ),
        )

    def load(cls, self, data: dict):
        super().load(self, data)
        self.input = ItemStack.from_dict(data.pop("input"))
        self.reagent = ItemStack.from_dict(data.pop("reagent"))
        self.output = ItemStack.from_dict(data.pop("output"))


class BrewingMixSchem1(RecipeSchem1):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "recipe",
                "brewing_mix1.json",
            ),
        )

    def load(cls, self, data: dict):
        super().load(self, data)
        self.input = ItemStack.from_dict(data.pop("input"))
        self.reagent = ItemStack.from_dict(data.pop("reagent"))
        self.output = ItemStack.from_dict(data.pop("output"))


class ShapedSchem1(RecipeSchem1):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__), "data", "schemas", "recipe", "shaped1.json"
            ),
        )

    def load(cls, self, data: dict):
        super().load(self, data)
        self.pattern = data.pop("pattern")
        self.key = {}
        for k, v in data.pop("key").items():
            self.key[k] = Ingredient.from_dict(v)

        res = data.pop("result")
        if isinstance(res, list):
            self.result = [ItemStack.from_dict(x) for x in res]
        else:
            self.result = ItemStack.from_dict(res)


class ShapelessSchem1(RecipeSchem1):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "recipe",
                "shapeless1.json",
            ),
        )

    def load(cls, self, data: dict):
        super().load(self, data)
        self.ingredients = [Ingredient.from_dict(x) for x in data.pop("ingredients")]
        self.result = ItemStack.from_dict(data.pop("result"))


class SmithingTransformSchem1(RecipeSchem1):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "recipe",
                "smithing_transform1.json",
            ),
        )

    def load(cls, self, data: dict):
        super().load(self, data)
        self.template = ItemStack.from_dict(data.pop("template"))
        self.base = ItemStack.from_dict(data.pop("base"))
        self.addition = ItemStack.from_dict(data.pop("addition"))
        self.result = ItemStack.from_dict(data.pop("result"))


class SmithingTransformSchem2(RecipeSchem1):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "recipe",
                "smithing_transform2.json",
            ),
        )

    def load(cls, self, data: dict):
        super().load(self, data)
        self.template = ItemStack("netherite_upgrade_smithing_template")
        self.base = ItemStack.from_dict(data.pop("base"))
        self.addition = ItemStack.from_dict(data.pop("addition"))
        self.result = ItemStack.from_dict(data.pop("result"))


class SmithingTrimSchem1(RecipeSchem1):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "recipe",
                "smithing_trim1.json",
            ),
        )

    def load(cls, self, data: dict):
        super().load(self, data)
        self.template = Ingredient.from_dict(data.pop("template"))
        self.base = Ingredient.from_dict(data.pop("base"))
        self.addition = Ingredient.from_dict(data.pop("addition"))


class MaterialReductionSchem1(RecipeSchem1):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "recipe",
                "material_reduction1.json",
            ),
        )

    def load(cls, self, data: dict):
        super().load(self, data)
        self.input = Ingredient.from_dict(data.pop("input"))
        self.output = [ItemStack.from_dict(x) for x in data.pop("output")]


class MaterialReductionSchem2(RecipeSchem1):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__),
                "data",
                "schemas",
                "recipe",
                "material_reduction1.json",
            ),
        )

    def load(cls, self, data: dict):
        super().load(self, data)
        self.input = Ingredient.from_dict(data.pop("input"))
        self.output = [ItemStack.from_dict(x) for x in data.pop("output")]
