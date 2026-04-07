__all__ = [
    "Direction",
    "Direction2d",
    "PackScope",
    "ItemGroup",
    "CameraListener",
    "Edition",
    "ModuleType",
    "CreativeCategory",
    "RenderMethod",
    "EventTarget",
    "UseAnimation",
    "BlockFace",
    "MapColor",
    "MapColour",
    "DyeColor",
    "DyeColour",
    "Formatting",
    "Color",
    "Colour",
    "Destination",
    "TextureType",
    "OxidationLevel",
    "RenderDistanceType",
    "Capability",
    "ProductType",
    "CurveType",
    "EntityPropertyType",
    "FilterTestType",
    "VibrationType",
    "LiquidTouchBehavior",
    "Difficulty",
    "EntityDamageSource",
    "DealsDamage",
    "DwellerRole",
    "EquipmentSlot",
    "LiquidMaterialType",
    "BaseEnum",
    "SupportShape",
    "PlacementDirectionState",
    "PlacementPositionState",
    "HomeRestrictionType",
    "LeashableSpringType",
    "LineOfSightObstructionType",
    "SetTargetType",
    "DismountMode",
    "ItemCooldownType",
    "EnchantableSlot",
    "SaturationModifierType",
    "ItemRarity",
    "DiscPlane",
    "CameraFacingMode",
    "BillboardDirectionMode",
    "MovementType",
    "MoveableSticky",
    "PrecipitationBehavior",
    "ConnectionState",
    "LerpMode",
    "LoopMode",
    "VersionBump",
    "PackageFormat",
    "TintMethod",
    "DirectionAll",
    "WearableSlot",
    "ClientEntityVariable",
    "TransportSearchStrategy",
    "TransportPlaceStrategy",
    "DashActionDirection",
    "Connections",
    "MultiBlockState",
    "DirectionVertical",
    "DiscDirection",
    "ControlFlags",
]

from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def parse(cls, value):
        if not value:
            return value
        return cls(value)


class ControlFlags(str, BaseEnum):
    JUMP = "jump"
    LOOK = "look"
    MOVE = "move"


class VillageType(str, BaseEnum):
    DEFAULT = "default"
    DESERT = "desert"
    ICE = "ice"
    SAVANNA = "savanna"
    TAIGA = "taiga"


class DashActionDirection(str, BaseEnum):
    PASSENGER = "passenger"


class TransportSearchStrategy(str, BaseEnum):
    NEAREST = "nearest"


class TransportPlaceStrategy(str, BaseEnum):
    WITH_MATCHING_OR_EMPTY = "with_matching_or_empty"


class ClientEntityVariable(str, BaseEnum):
    PUBLIC = "public"


class WearableSlot(str, BaseEnum):
    NONE = "none"
    BODY = "slot.armor.body"
    CHEST = "slot.armor.chest"
    FEET = "slot.armor.feet"
    HEAD = "slot.armor.head"
    LEGS = "slot.armor.legs"
    OFFHAND = "slot.weapon.offhand"


class TintMethod(str, BaseEnum):
    NONE = "none"
    DEFAULT_FOLIAGE = "default_foliage"
    BIRCH_FOLIAGE = "birch_foliage"
    EVERGREEN_FOLIAGE = "evergreen_foliage"
    DRY_FOLIAGE = "dry_foliage"
    GRASS = "grass"
    WATER = "water"


class PackageFormat(str, BaseEnum):
    MCADDON = "mcaddon"
    MCPACK = "mcpack"
    MCWORLD = "mcworld"
    MCTEMPLATE = "mctemplate"
    PARTNER = "partner"

    # Unused
    # MCPROJECT = "mcproject"
    # MCSTRUCTURE = "mcstructure"


class VersionBump(str, BaseEnum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


class LoopMode(str, BaseEnum):
    HOLD_ON_LAST_FRAME = "hold_on_last_frame"


class LerpMode(str, BaseEnum):
    CATMULLROM = "catmullrom"


class PrecipitationBehavior(str, BaseEnum):
    OBRAIN = "obrain"
    OBSTRUCT_RAIN_ACCUMULATE_SNOW = "obstruct_rain_accumulate_snow"
    NONE = "none"


class MovementType(str, BaseEnum):
    PUSH_PULL = "push_pull"
    PUSH = "push"
    POPPED = "popped"
    IMMOVABLE = "immovable"


class MoveableSticky(str, BaseEnum):
    SAME = "same"
    NONE = "none"


class CameraFacingMode(str, BaseEnum):
    ROTATE_XYZ = "rotate_xyz"
    ROTATE_Y = "rotate_y"
    LOOKAT_XYZ = "lookat_xyz"
    LOOKAT_Y = "lookat_y"
    DIRECTION_X = "direction_x"
    DIRECTION_Y = "direction_y"
    DIRECTION_Z = "direction_z"
    LOOKAT_DIRECTION = "lookat_direction"
    EMITTER_TRANSFORM_XZ = "emitter_transform_xz"


class BillboardDirectionMode(str, BaseEnum):
    DERIVE_FROM_VELOCITY = "derive_from_velocity"
    CUSTOM_DIRECTION = "custom_direction"
    CUSTOM = "custom"


class DiscPlane(str, BaseEnum):
    Y = "y"


class DiscDirection(str, BaseEnum):
    OUTWARDS = "outwards"


class ItemRarity(str, BaseEnum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"


class SaturationModifierType(str, BaseEnum):
    SUPERNATURAL = "supernatural"
    NORMAL = "normal"
    LOW = "low"
    POOR = "poor"
    GOOD = "good"


class EnchantableSlot(str, BaseEnum):
    ALL = "all"
    MELEE_SPEAR = "melee_spear"
    AXE = "axe"
    BOW = "bow"
    CROSSBOW = "crossbow"
    SPEAR = "spear"
    ARMOR_FEET = "armor_feet"
    ARMOR_TORSO = "armor_torso"
    ARMOR_HEAD = "armor_head"
    ARMOR_LEGS = "armor_legs"
    HOE = "hoe"
    PICKAXE = "pickaxe"
    SHOVEL = "shovel"
    ELYTRA = "elytra"
    FISHING_ROD = "fishing_rod"
    FLINTSTEEL = "flintsteel"
    SWORD = "sword"
    SHIELD = "shield"
    SHEARS = "shears"
    COSMETIC_HEAD = "cosmetic_head"
    CARROTSTICK = "carrotstick"


class ItemCooldownType(str, BaseEnum):
    ATTACK = "attack"
    USE = "use"


class DismountMode(str, BaseEnum):
    DEFAULT = "default"
    ON_TOP_CENTER = "on_top_center"


class LineOfSightObstructionType(str, BaseEnum):
    COLLISION = "collision"
    OUTLINE = "outline"
    COLLISION_FOR_CAMERA = "collision_for_camera"


class SetTargetType(str, BaseEnum):
    NEVER = "never"
    ONCE_AND_STOP_SCANNING = "once_and_stop_scanning"
    ONCE_AND_KEEP_SCANNING = "once_and_keep_scanning"


class LeashableSpringType(str, BaseEnum):
    BOUNCY = "bouncy"
    DAMPENED = "dampened"
    QUAD_DAMPENED = "quad_dampened"


class HomeRestrictionType(str, BaseEnum):
    NONE = "none"
    RANDOM_MOVEMENT = "random_movement"
    ALL_MOVEMENT = "all_movement"


class PlacementDirectionState(str, BaseEnum):
    CARDINAL_DIRECTION = "minecraft:cardinal_direction"
    FACING_DIRECTION = "minecraft:facing_direction"
    CORNER_AND_CARDINAL_DIRECTION = "minecraft:corner_and_cardinal_direction"


class PlacementPositionState(str, BaseEnum):
    BLOCK_FACE = "minecraft:block_face"
    VERTICAL_HALF = "minecraft:vertical_half"


class ConnectionState(str, BaseEnum):
    CARDINAL_CONNECTIONS = "minecraft:cardinal_connections"


class MultiBlockState(str, BaseEnum):
    MULTI_BLOCK_PART = "minecraft:multi_block_part"


class DirectionVertical(str, BaseEnum):
    UP = "up"
    DOWN = "down"


class SupportShape(str, BaseEnum):
    FENCE = "fence"
    STAIR = "stair"


class LiquidMaterialType(str, BaseEnum):
    LAVA = "lava"
    WATER = "water"
    ANY = "any"

    @classmethod
    def parse(cls, value):
        return cls(str(value).lower())


class DwellerRole(str, BaseEnum):
    PASSIVE = "passive"
    HOSTILE = "hostile"
    DEFENDER = "defender"
    INHABITANT = "inhabitant"


class DealsDamage(str, BaseEnum):
    YES = "yes"
    NO = "no"
    NO_BUT_SIDE_EFFECTS_APPLY = "no_but_side_effects_apply"


class EntityDamageSource(str, BaseEnum):
    ALL = "all"
    ANVIL = "anvil"
    BLOCK_EXPLOSION = "block_explosion"
    CAMPFIRE = "campfire"
    CHARGING = "charging"
    CONTACT = "contact"
    DROWNING = "drowning"
    ENTITY_ATTACK = "entity_attack"
    ENTITY_EXPLOSION = "entity_explosion"
    FALL = "fall"
    FALLING_BLOCK = "falling_block"
    FIRE = "fire"
    FIRE_TICK = "fire_tick"
    FIREWORKS = "fireworks"
    FLY_INTO_WALL = "fly_into_wall"
    FREEZING = "freezing"
    LAVA = "lava"
    LIGHTNING = "lightning"
    MACE_SMASH = "mace_smash"
    MAGIC = "magic"
    MAGMA = "magma"
    NONE = "none"
    OVERRIDE = "override"
    PISTON = "piston"
    PROJECTILE = "projectile"
    RAM_ATTACK = "ram_attack"
    SELF_DESTRUCT = "self_destruct"
    SONIC_BOOM = "sonic_boom"
    SOUL_CAMPFIRE = "soul_campfire"
    STALACTITE = "stalactite"
    STALAGMITE = "stalagmite"
    STARVE = "starve"
    SUFFOCATION = "suffocation"
    TEMPERATURE = "temperature"
    THORNS = "thorns"
    VOID = "void"
    WITHER = "wither"


class Difficulty(str, BaseEnum):
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"


# TODO: Find all values.
class FilterTestType(str, BaseEnum):
    IS_TAMED = "is_tamed"
    IS_CONTROLLING_PASSENGER_FAMILY = "is_controlling_passenger_family"
    IS_VEHICLE_FAMILY = "is_vehicle_family"
    X_ROTATION = "x_rotation"
    Y_ROTATION = "y_rotation"
    Z_ROTATION = "z_rotation"
    ACTOR_HEALTH = "actor_health"
    ALL_SLOTS_EMPTY = "all_slots_empty"
    ANY_SLOT_EMPTY = "any_slot_empty"
    BOOL_PROPERTY = "bool_property"
    CLOCK_TIME = "clock_time"
    DISTANCE_TO_NEAREST_PLAYER = "distance_to_nearest_player"
    ENUM_PROPERTY = "enum_property"
    FLOAT_PROPERTY = "float_property"
    HAS_ABILITY = "has_ability"
    HAS_BIOME_TAG = "has_biome_tag"
    HAS_COMPONENT = "has_component"
    HAS_CONTAINER_OPEN = "has_container_open"
    HAS_DAMAGE = "has_damage"
    HAS_DAMAGED_EQUIPMENT = "has_damaged_equipment"
    HAS_EQUIPMENT = "has_equipment"
    HAS_EQUIPMENT_TAG = "has_equipment_tag"
    HAS_MOB_EFFECT = "has_mob_effect"
    HAS_NAMETAG = "has_nametag"
    HAS_PROPERTY = "has_property"
    HAS_RANGED_WEAPON = "has_ranged_weapon"
    HAS_SILK_TOUCH = "has_silk_touch"
    HAS_TAG = "has_tag"
    HAS_TARGET = "has_target"
    HAS_TRADE_SUPPLY = "has_trade_supply"
    HOME_DISTANCE = "home_distance"
    HOURLY_CLOCK_TIME = "hourly_clock_time"
    INACTIVITY_TIMER = "inactivity_timer"
    INT_PROPERTY = "int_property"
    IN_BLOCK = "in_block"
    IN_CARAVAN = "in_caravan"
    IN_CLOUDS = "in_clouds"
    IN_CONTACT_WITH_WATER = "in_contact_with_water"
    IN_LAVA = "in_lava"
    IN_NETHER = "in_nether"
    IN_OVERWORLD = "in_overworld"
    IN_WATER = "in_water"
    IN_WATER_OR_RAIN = "in_water_or_rain"
    IS_ALTITUDE = "is_altitude"
    IS_AVOIDING_MOBS = "is_avoiding_mobs"
    IS_BABY = "is_baby"
    IS_BIOME = "is_biome"
    IS_BLOCK = "is_block"
    IS_BOUND_TO_CREAKING_HEART = "is_bound_to_creaking_heart"
    IS_BRIGHTNESS = "is_brightness"
    IS_CLIMBING = "is_climbing"
    IS_COLOR = "is_color"
    IS_DAYTIME = "is_daytime"
    IS_DIFFICULTY = "is_difficulty"
    IS_FAMILY = "is_family"
    IS_GAME_RULE = "is_game_rule"
    IS_HUMID = "is_humid"
    IS_IMMOBILE = "is_immobile"
    IS_IN_VILLAGE = "is_in_village"
    IS_LEASHED = "is_leashed"
    IS_LEASHED_TO = "is_leashed_to"
    IS_MARK_VARIANT = "is_mark_variant"
    IS_MISSING_HEALTH = "is_missing_health"
    IS_MOVING = "is_moving"
    IS_NAVIGATING = "is_navigating"
    IS_OWNER = "is_owner"
    IS_PANICKING = "is_panicking"
    IS_PERSISTENT = "is_persistent"
    IS_RAIDER = "is_raider"
    IS_RIDING = "is_riding"
    IS_RIDING_SELF = "is_riding_self"
    IS_SITTING = "is_sitting"
    IS_SKIN_ID = "is_skin_id"
    IS_SLEEPING = "is_sleeping"
    IS_SNEAKING = "is_sneaking"
    IS_SNEAK_HELD = "is_sneak_held"
    IS_SNOW_COVERED = "is_snow_covered"
    IS_SPRINTING = "is_sprinting"
    IS_TARGET = "is_target"
    IS_TEMPERATURE_TYPE = "is_temperature_type"
    IS_TEMPERATURE_VALUE = "is_temperature_value"
    IS_UNDERGROUND = "is_underground"
    IS_UNDERWATER = "is_underwater"
    IS_VARIANT = "is_variant"
    IS_VISIBLE = "is_visible"
    IS_WATERLOGGED = "is_waterlogged"
    IS_WEATHER = "is_weather"
    LIGHT_LEVEL = "light_level"
    MOON_INTENSITY = "moon_intensity"
    MOON_PHASE = "moon_phase"
    ON_FIRE = "on_fire"
    ON_GROUND = "on_ground"
    ON_HOT_BLOCK = "on_hot_block"
    ON_LADDER = "on_ladder"
    OWNER_DISTANCE = "owner_distance"
    RANDOM_CHANCE = "random_chance"
    RIDER_COUNT = "rider_count"
    SURFACE_MOB = "surface_mob"
    TAKING_FIRE_DAMAGE = "taking_fire_damage"
    TARGET_DISTANCE = "target_distance"
    TRUSTS = "trusts"
    WAS_LAST_HURT_BY = "was_last_hurt_by"
    WEATHER = "weather"
    WEATHER_AT_POSITION = "weather_at_position"


# TODO: Find all values.
class VibrationType(str, BaseEnum):
    ENTITY_ACT = "entity_act"
    ENTITY_DIE = "entity_die"


class EntityPropertyType(str, BaseEnum):
    FLOAT = "float"
    INT = "int"
    BOOL = "bool"
    ENUM = "enum"


class CurveType(str, BaseEnum):
    LINEAR = "linear"
    BEZIER = "bezier"
    CATMULL_ROM = "catmull_rom"


class ProductType(str, BaseEnum):
    ADDON = "addon"


class Capability(str, BaseEnum):
    CHEMISTRY = "chemistry"
    EDITOR_EXTENSION = "editorExtension"
    EXPERIMENTAL_CUSTOM_UI = "experimental_custom_ui"
    RAYTRACED = "raytraced"
    PBR = "pbr"


class RenderDistanceType(str, BaseEnum):
    FIXED = "fixed"
    RENDER = "render"


class Connections(str, BaseEnum):
    ALL = "all"
    ONLY_FENCES = "only_fences"
    NONE = "none"


class Direction(str, BaseEnum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    UP = "up"
    DOWN = "down"


class Direction2d(str, BaseEnum):
    """
    Direction without UP and DOWN.
    """

    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


class DirectionAll(str, BaseEnum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    UP = "up"
    DOWN = "down"
    ALL = "all"


class PackScope(str, BaseEnum):
    WORLD = "world"
    ADDON = "addon"


class ItemGroup(str, BaseEnum):
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


class CameraListener(str, BaseEnum):
    NONE = "none"
    PLAYER = "player"


class Edition(str, BaseEnum):
    BEDROCK = "bedrock"
    PREVIEW = "preview"
    EDUCATION = "education"


class ModuleType(str, BaseEnum):
    DATA = "data"
    RESOURCES = "resources"
    CLIENT_DATA = "client_data"
    INTERFACE = "interface"
    SCRIPT = "script"
    SKIN_PACK = "skin_pack"
    WORLD_TEMPLATE = "world_template"

    def get_pack_type(self) -> str | None:
        match self._value_:
            case "data":
                return "behavior_pack"
            case "resources":
                return "resource_pack"
            case "skin_pack":
                return "skin_pack"
        return None


class CreativeCategory(str, BaseEnum):
    COMMANDS = "commands"
    CONSTRUCTION = "construction"
    EQUIPMENT = "equipment"
    ITEMS = "items"
    NATURE = "nature"
    NONE = "none"


class LiquidTouchBehavior(str, BaseEnum):
    BLOCKING = "blocking"
    BROKEN = "broken"
    POPPED = "popped"
    NO_REACTION = "no_reaction"


class RenderMethod(str, BaseEnum):
    OPAQUE = "opaque"
    DOUBLE_SIDED = "double_sided"
    BLEND = "blend"
    ALPHA_TEST = "alpha_test"
    ALPHA_TEST_SINGLE_SIDED = "alpha_test_single_sided"


class EventTarget(str, BaseEnum):
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


class UseAnimation(str, BaseEnum):
    EAT = "eat"
    DRINK = "drink"
    CAMERA = "camera"


class BlockFace(str, BaseEnum):
    UP = "up"
    DOWN = "down"
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    SIDE = "side"
    ALL = "all"


class MapColor(str, BaseEnum):
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


MapColour = MapColor


class DyeColor(str, BaseEnum):
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

    def build(self) -> str:
        return str(self._value_[0])

    @staticmethod
    def model_validate(data: str) -> "Formatting":
        try:
            return Formatting[data]
        except KeyError:
            raise ValueError(f"Invalid Formatting value: {data}")


class Color(str, BaseEnum):
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


Colour = Color


class Destination(str, BaseEnum):
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


class TextureType(str, BaseEnum):
    terrain = "terrain"
    item = "item"


class OxidationLevel(str, BaseEnum):
    UNAFFECTED = "unaffected"
    EXPOSED = "exposed"
    WEATHERED = "weathered"
    OXIDIZED = "oxidized"


class EquipmentSlot(str, BaseEnum):
    MAINHAND = "slot.weapon.mainhand"
    OFFHAND = "slot.weapon.offhand"
    HEAD = "slot.armor.head"
    CHEST = "slot.armor.chest"
    LEGS = "slot.armor.legs"
    FEET = "slot.armor.feet"
    BODY = "slot.armor.body"
