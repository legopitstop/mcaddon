from enum import Enum


class RecipeTag(Enum):
    CRAFTING_TABLE = "crafting_table"
    BREWING_STAND = "brewing_stand"
    SMITHING_TABLE = "smithing_table"
    CAMPFIRE = "campfire"
    SOUL_CAMPFIRE = "soul_campfire"
    FURNACE = "furnace"
    SMOKER = "smoker"
    STONECUTTER = "stonecutter"
    MATERIAL_REDUCER = "material_reducer"


class CameraListener(Enum):
    none = "none"
    player = "player"


class Edition(Enum):
    bedrock = "bedrock"
    preview = "preview"
    education = "education"


class ModuleType(Enum):
    resources = "resources"
    data = "data"
    client_data = "client_data"
    interface = "interface"
    world_template = "world_template"


class Category(Enum):
    commands = "commands"
    construction = "construction"
    equipment = "equipment"
    items = "items"
    nature = "nature"
    none = "none"


class RenderMethod(Enum):
    opaque = "opaque"
    double_sided = "double_sided"
    blend = "blend"
    alpha_test = "alpha_test"


class EventTarget(Enum):
    self = "self"
    holder = "holder"
    baby = "baby"
    other = "other"
    player = "player"
    target = "target"
    parent = "parent"
    block = "block"
    damager = "damager"
    item = "item"


class UseAnimation(Enum):
    eat = "eat"
    drink = "drink"
    camera = "camera"


class RecipeTag(Enum):
    furnace = "furnace"
    smoker = "smoker"
    campfire = "campfire"
    soul_campfire = "soul_campfire"
    crafting_table = "crafting_table"
    brewing_stand = "brewing_stand"
    stonecutter = "stonecutter"
    smithing_table = "smithing_table"
    material_reducer = "material_reducer"


class BlockFace(Enum):
    up = "up"
    down = "down"
    north = "north"
    south = "south"
    east = "east"
    west = "west"
    side = "side"
    all = "all"


class Color(Enum):
    white = "white"
    light_gray = "light_gray"
    gray = "gray"
    black = "black"
    brown = "brown"
    red = "red"
    orange = "orange"
    yellow = "yellow"
    lime = "lime"
    green = "green"
    cyan = "cyan"
    light_blue = "light_blue"
    blue = "blue"
    purple = "purple"
    magenta = "magenta"
    pink = "pink"


class Destination(Enum):
    buriedtreasure = "buriedtreasure"
    endcity = "endcity"
    fortress = "fortress"
    mansion = "mansion"
    mineshaft = "mineshaft"
    monument = "monument"
    pillageroutpost = "pillageroutpost"
    ruins = "ruins"
    shipwreck = "shipwreck"
    stronghold = "stronghold"
    temple = "temple"
    village = "village"


class TextureType(Enum):
    terrain = "terrain"
    item = "item"


class OxidationLevel(Enum):
    unaffected = "unaffected"
    exposed = "exposed"
    weathered = "weathered"
    oxidized = "oxidized"


class LootContextType(Enum):
    empty = "empty"
    chest = "chest"
    command = "command"
    selector = "selector"
    fishing = "fishing"
    entity = "entity"
    archaeology = "archaeology"
    gift = "gift"
    barter = "barter"
    advancement_reward = "advancement_reward"
    advancement_entity = "advancement_entity"
    advancement_location = "advancement_location"
    generic = "generic"
    block = "block"
