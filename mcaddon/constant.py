from typing import Self
from enum import Enum


class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    UP = "up"
    DOWN = "down"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return Direction(data)
        except KeyError:
            raise ValueError(f"Invalid Direction value: {data}")


class PackScope(Enum):
    WORLD = "world"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return PackScope[data]
        except KeyError:
            raise ValueError(f"Invalid PackScope value: {data}")


class ItemGroup(Enum):
    SEARCH = "itemGroup.search"
    PLANKS = "itemGroup.name.planks"
    WALLS = "itemGroup.name.walls"
    FENCE = "itemGroup.name.fence"
    FENCE_GATE = "itemGroup.name.fenceGate"
    STAIRS = "itemGroup.name.stairs"
    DOOR = "itemGroup.name.door"
    GLASS = "itemGroup.name.glass"
    GLASS_PANE = "itemGroup.name.glassPane"
    PERMISSION = "itemGroup.name.permission"
    SLABS = "itemGroup.name.slab"
    STONE_BRICKS = "itemGroup.name.stoneBrick"
    SANDSTONE = "itemGroup.name.sandstone"
    WOOL = "itemGroup.name.wool"
    CARPET = "itemGroup.name.woolCarpet"
    CONCRETE_POWDER = "itemGroup.name.concretePowder"
    CONCRETE = "itemGroup.name.concrete"
    STAINED_TERRACOTTA = "itemGroup.name.stainedClay"
    GLAZED_TERRACOTTA = "itemGroup.name.glazedTerracotta"
    DYE = "itemGroup.name.dye"
    ORE = "itemGroup.name.ore"
    STONE = "itemGroup.name.stone"
    LOG = "itemGroup.name.log"
    LEAVES = "itemGroup.name.leaves"
    SAPLINGS = "itemGroup.name.sapling"
    SEED = "itemGroup.name.seed"
    CROP = "itemGroup.name.crop"
    GRASS = "itemGroup.name.grass"
    FLOWER = "itemGroup.name.flower"
    RAW_FOOD = "itemGroup.name.rawFood"
    COOKED_FOOD = "itemGroup.name.cookedFood"
    MISC_FOOD = "itemGroup.name.miscFood"
    MUSHROOM = "itemGroup.name.mushroom"
    MONSTER_STONE_EGG = "itemGroup.name.monsterStoneEgg"
    MOB_EGG = "itemGroup.name.mobEgg"
    HELMET = "itemGroup.name.helmet"
    CHESTPLATE = "itemGroup.name.chestplate"
    LEGGINGS = "itemGroup.name.leggings"
    BOOTS = "itemGroup.name.boots"
    HORSE_ARMOR = "itemGroup.name.horseArmor"
    SWORD = "itemGroup.name.sword"
    AXE = "itemGroup.name.axe"
    PICKAXE = "itemGroup.name.pickaxe"
    SHOVEL = "itemGroup.name.shovel"
    HOE = "itemGroup.name.hoe"
    ARROW = "itemGroup.name.arrow"
    POTION = "itemGroup.name.potion"
    SPLASH_POTION = "itemGroup.name.splashPotion"
    LINGERING_POTION = "itemGroup.name.lingeringPotion"
    BED = "itemGroup.name.bed"
    CHALKBOARD = "itemGroup.name.chalkboard"
    ANVIL = "itemGroup.name.anvil"
    CHEST = "itemGroup.name.chest"
    SHULKER_BOX = "itemGroup.name.shulkerBox"
    RECORD = "itemGroup.name.record"
    SKULL = "itemGroup.name.skull"
    BOAT = "itemGroup.name.boat"
    RAIL = "itemGroup.name.rail"
    MINECRART = "itemGroup.name.minecart"
    PRESSURE_PLATE = "itemGroup.name.pressurePlate"
    TRAPDOOR = "itemGroup.name.trapdoor"
    ENCHANTED_BOOK = "itemGroup.name.enchantedBook"
    BANNER = "itemGroup.name.banner"
    FIREWORK = "itemGroup.name.firework"
    FIREWORK_STARS = "itemGroup.name.fireworkStars"
    CORAL = "itemGroup.name.coral"
    CORAL_DECORATIONS = "itemGroup.name.coral_decorations"
    BUTTON = "itemGroup.name.button"
    SIGN = "itemGroup.name.sign"
    WOOD = "itemGroup.name.wood"
    BANNER_PATTERN = "itemGroup.name.banner_pattern"
    NETHER_WART_BLOCK = "itemGroup.name.netherWartBlock"
    CANDLES = "itemGroup.name.candles"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return ItemGroup(data)
        except KeyError:
            raise ValueError(f"Invalid ItemGroup value: {data}")


class CameraListener(Enum):
    NONE = "none"
    PLAYER = "player"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return CameraListener(data)
        except KeyError:
            raise ValueError(f"Invalid CameraListener value: {data}")


class Edition(Enum):
    BEDROCK = "bedrock"
    PREVIEW = "preview"
    EDUCATION = "education"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return Edition(data)
        except KeyError:
            raise ValueError(f"Invalid Edition value: {data}")


class ModuleType(Enum):
    RESOURCES = "resources"
    DATA = "data"
    CLIENT_DATA = "client_data"
    INTERFACE = "interface"
    WORLD_TEMPLATE = "world_template"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return ModuleType(data)
        except KeyError:
            raise ValueError(f"Invalid ModuleType value: {data}")


class Category(Enum):
    COMMANDS = "commands"
    CONSTRUCTION = "construction"
    EQUIPMENT = "equipment"
    ITEMS = "items"
    NATURE = "nature"
    NONE = "none"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return Category(data)
        except KeyError:
            raise ValueError(f"Invalid Category value: {data}")


class RenderMethod(Enum):
    OPAQUE = "opaque"
    DOUBLE_SIDED = "double_sided"
    BLEND = "blend"
    ALPHA_TEST = "alpha_test"
    ALPHA_TEST_SINGLE_SIDED = "alpha_test_single_sided"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return RenderMethod(data)
        except KeyError:
            raise ValueError(f"Invalid RenderMethod value: {data}")


class EventTarget(Enum):
    SELF = "self"
    HOLDER = "holder"
    BABY = "baby"
    OTHER = "other"
    PLAYER = "player"
    TARGET = "target"
    PARENT = "parent"
    BLOCK = "block"
    DAMAGER = "damager"
    ITEM = "item"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return EventTarget(data)
        except KeyError:
            raise ValueError(f"Invalid EventTarget value: {data}")


class UseAnimation(Enum):
    EAT = "eat"
    DRINK = "drink"
    CAMERA = "camera"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return UseAnimation(data)
        except KeyError:
            raise ValueError(f"Invalid UseAnimation value: {data}")


class BlockFace(Enum):
    UP = "up"
    DOWN = "down"
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    SIDE = "side"
    ALL = "all"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return BlockFace(data)
        except KeyError:
            raise ValueError(f"Invalid BlockFace value: {data}")


class MapColor(Enum):
    CLEAR = "#0"
    PALE_GREEN = "#7FB238"
    PALE_YELLOW = "#F7E9A3"
    WHITE_GRAY = "#C7C7C7"
    BRIGHT_RED = "#FF0000"
    PALE_PURPLE = "#A0A0FF"
    IRON_GRAY = "#A7A7A7"
    DARK_GREEN = "#7C00"
    WHITE = "#FFFFFF"
    LIGHT_BLUE_GRAY = "#A4A8B8"
    DIRT_BROWN = "#976D4D"
    STONE_GRAY = "#707070"
    WATER_BLUE = "#4040FF"
    OAK_TAN = "#8F7748"
    OFF_WHITE = "#FFFCF5"
    ORANGE = "#D87F33"
    MAGENTA = "#B24CD8"
    LIGHT_BLUE = "#6699D8"
    YELLOW = "#E5E533"
    LIME = "#7FCC19"
    PINK = "#F27FA5"
    GRAY = "#4C4C4C"
    LIGHT_GRAY = "#999999"
    CYAN = "#4C7F99"
    PURPLE = "#7F3FB2"
    BLUE = "#334CB2"
    BROWN = "#664C33"
    GREEN = "#667F33"
    RED = "#993333"
    BLACK = "#191919"
    GOLD = "#FAEE4D"
    DIAMOND_BLUE = "#5CDBD5"
    LAPIS_BLUE = "#4A80FF"
    EMERALD_GREEN = "#D93A"
    SPRUCE_BROWN = "#815631"
    DARK_RED = "#700200"
    TERRACOTTA_WHITE = "#D1B1A1"
    TERRACOTTA_ORANGE = "#9F5224"
    TERRACOTTA_MAGENTA = "#95576C"
    TERRACOTTA_LIGHT_BLUE = "#706C8A"
    TERRACOTTA_YELLOW = "#BA8524"
    TERRACOTTA_LIME = "#677535"
    TERRACOTTA_PINK = "#A04D4E"
    TERRACOTTA_GRAY = "#392923"
    TERRACOTTA_LIGHT_GRAY = "#876B62"
    TERRACOTTA_CYAN = "#575C5C"
    TERRACOTTA_PURPLE = "#7A4958"
    TERRACOTTA_BLUE = "#4C3E5C"
    TERRACOTTA_BROWN = "#4C3223"
    TERRACOTTA_GREEN = "#4C522A"
    TERRACOTTA_RED = "#8E3C2E"
    TERRACOTTA_BLACK = "#251610"
    DULL_RED = "#BD3031"
    DULL_PINK = "#943F61"
    DARK_CRIMSON = "#5C191D"
    TEAL = "#167E86"
    DARK_AQUA = "#3A8E8C"
    DARK_DULL_PINK = "#562C3E"
    BRIGHT_TEAL = "#14B485"
    DEEPSLATE_GRAY = "#646464"
    RAW_IRON_PINK = "#D8AF93"
    LICHEN_GREEN = "#7FA796"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return MapColor(data)
        except KeyError:
            raise ValueError(f"Invalid MapColor value: {data}")


MapColour = MapColor


class DyeColor(Enum):
    WHITE = MapColor.WHITE
    LIGHT_GRAY = MapColor.LIGHT_GRAY
    GRAY = MapColor.GRAY
    BLACK = MapColor.BLACK
    BROWN = MapColor.BROWN
    RED = MapColor.RED
    ORANGE = MapColor.ORANGE
    YELLOW = MapColor.YELLOW
    LIME = MapColor.LIME
    GREEN = MapColor.GREEN
    CYAN = MapColor.CYAN
    LIGHT_BLUE = MapColor.LIGHT_BLUE
    BLUE = MapColor.BLUE
    PURPLE = MapColor.PURPLE
    MAGENTA = MapColor.MAGENTA
    PINK = MapColor.PINK

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return DyeColor(data)
        except KeyError:
            raise ValueError(f"Invalid DyeColor value: {data}")


DyeColour = DyeColor


class Formatting(Enum):
    DARK_RED = ("§4", "\\u00A74", "#BE0000")
    RED = ("§C", "\\u00A7C", "#FE3F3F")
    GOLD = ("§6", "\\u00A76", "#D9A334")
    YELLOW = ("§E", "\\u00A7E", "#FEFE3F")
    DARK_GREEN = ("§2", "\\u00A72", "#00BE00")
    GREEN = ("§A", "\\u00A7A", "#3FFE3F")
    AQUA = ("§B", "\\u00A7B", "#3FFEFE")
    DARK_AQUA = ("§3", "\\u00A73", "#00BEBE")
    DARK_BLUE = ("§1", "\\u00A71", "#0000BE")
    BLUE = ("§9", "\\u00A79", "#3F3FFE")
    LIGHT_PURPLE = ("§D", "\\u00A7D", "#FE3FFE")
    DARK_PURPLE = ("§5", "\\u00A75", "#BE00BE")
    WHITE = ("§F", "\\u00A7F", "#FFFFFF")
    GRAY = ("§7", "\\u00A77", "#BEBEBE")
    DARK_GRAY = ("§8", "\\u00A78", "#3F3F3F")
    BLACK = ("§0", "\\u00A70", "#000000")
    RESET = ("§R", "\\u00A7R", None)
    BOLD = ("§L", "\\u00A7L", None)
    ITALIC = ("§O", "\\u00A7O", None)
    UNDERLINE = ("§N", "\\u00A7N", None)
    STRIKE = ("§M", "\\u00A7M", None)
    OBFUSCATE = ("§K", "\\u00A7K", None)

    def jsonify(self) -> dict:
        return self._value_[2]

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return Formatting[data]
        except KeyError:
            raise ValueError(f"Invalid Formatting value: {data}")


class Color(Enum):
    WHITE = "white"
    LIGHT_GRAY = "light_gray"
    GRAY = "gray"
    BLACK = "black"
    BROWN = "brown"
    RED = "red"
    ORANGE = "orange"
    YELLOW = "yellow"
    LIME = "lime"
    GREEN = "green"
    CYAN = "cyan"
    LIGHT_BLUE = "light_blue"
    BLUE = "blue"
    PURPLE = "purple"
    MAGENTA = "magenta"
    PINK = "pink"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return Color(data)
        except KeyError:
            raise ValueError(f"Invalid Color value: {data}")


Colour = Color


class Destination(Enum):
    BURIEDTREASURE = "buriedtreasure"
    ENDCITY = "endcity"
    FORTRESS = "fortress"
    MANSION = "mansion"
    MINESHAFT = "mineshaft"
    MOMUMENT = "monument"
    PILLAGEROUTPOST = "pillageroutpost"
    RUINS = "ruins"
    SHIPWRECK = "shipwreck"
    STRONGHOLD = "stronghold"
    TEMPLE = "temple"
    VILLAGE = "village"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return Destination(data)
        except KeyError:
            raise ValueError(f"Invalid Destination value: {data}")


class TextureType(Enum):
    terrain = "terrain"
    item = "item"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return TextureType(data)
        except KeyError:
            raise ValueError(f"Invalid TextureType value: {data}")


class OxidationLevel(Enum):
    UNAFFECTED = "unaffected"
    EXPOSED = "exposed"
    WEATHERED = "weathered"
    OXIDIZED = "oxidized"

    def jsonify(self) -> dict:
        return self._value_

    @staticmethod
    def from_dict(data: str) -> Self:
        try:
            return OxidationLevel(data)
        except KeyError:
            raise ValueError(f"Invalid OxidationLevel value: {data}")
