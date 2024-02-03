from .. import Schema, ItemStack, Ingredient


class FurnaceSchem1(Schema):
    def __init__(self):
        Schema.__init__(self, "furnace1.json")

    def load(cls, self, data: dict):
        self.input = Ingredient.from_dict(data.pop("input"))
        self.output = ItemStack.from_dict(data.pop("output"))


class BrewingContainerSchem1(Schema):
    def __init__(self):
        Schema.__init__(self, "brewing_container1.json")

    def load(cls, self, data: dict):
        self.input = ItemStack.from_dict(data.pop("input"))
        self.reagent = ItemStack.from_dict(data.pop("reagent"))
        self.output = ItemStack.from_dict(data.pop("output"))


class BrewingMixSchem1(Schema):
    def __init__(self):
        Schema.__init__(self, "brewing_mix1.json")

    def load(cls, self, data: dict):
        self.input = ItemStack.from_dict(data.pop("input"))
        self.reagent = ItemStack.from_dict(data.pop("reagent"))
        self.output = ItemStack.from_dict(data.pop("output"))


class ShapedSchem1(Schema):
    def __init__(self):
        Schema.__init__(self, "shaped1.json")

    def load(cls, self, data: dict):
        self.pattern = data.pop("pattern")
        self.key = {}
        for k, v in data.pop("key").items():
            self.key[k] = Ingredient.from_dict(v)

        res = data.pop("result")
        if isinstance(res, list):
            self.result = [ItemStack.from_dict(x) for x in res]
        else:
            self.result = ItemStack.from_dict(res)


class ShapelessSchem1(Schema):
    def __init__(self):
        Schema.__init__(self, "shapeless1.json")

    def load(cls, self, data: dict):
        self.ingredients = [Ingredient.from_dict(x) for x in data.pop("ingredients")]
        self.result = ItemStack.from_dict(data.pop("result"))


class SmithingTransformSchem1(Schema):
    def __init__(self):
        Schema.__init__(self, "smithing_transform1.json")

    def load(cls, self, data: dict):
        self.template = ItemStack.from_dict(data.pop("template"))
        self.base = ItemStack.from_dict(data.pop("base"))
        self.addition = ItemStack.from_dict(data.pop("addition"))
        self.result = ItemStack.from_dict(data.pop("result"))


class SmithingTransformSchem2(Schema):
    def __init__(self):
        Schema.__init__(self, "smithing_transform2.json")

    def load(cls, self, data: dict):
        self.template = ItemStack("netherite_upgrade_smithing_template")
        self.base = ItemStack.from_dict(data.pop("base"))
        self.addition = ItemStack.from_dict(data.pop("addition"))
        self.result = ItemStack.from_dict(data.pop("result"))


class SmithingTrimSchem1(Schema):
    def __init__(self):
        Schema.__init__(self, "smithing_trim1.json")

    def load(cls, self, data: dict):
        self.template = Ingredient.from_dict(data.pop("template"))
        self.base = Ingredient.from_dict(data.pop("base"))
        self.addition = Ingredient.from_dict(data.pop("addition"))


class MaterialReductionSchem1(Schema):
    def __init__(self):
        Schema.__init__(self, "material_reduction1.json")

    def load(cls, self, data: dict): ...
