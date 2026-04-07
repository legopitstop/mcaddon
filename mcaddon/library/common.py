__all__ = ["MenuCategory", "MenuCategories", "BaseDescription"]

from typing import Optional
from pydantic import field_validator

from mcaddon.core.base import BaseModel
from .constants import CreativeCategory


class MenuCategory(BaseModel):
    category: Optional[CreativeCategory]
    group: Optional[str] = None
    is_hidden_in_commands: bool = False

    @field_validator("category", mode="before")
    @classmethod
    def coerce_enum(cls, v):
        return CreativeCategory.parse(v.lower())


class MenuCategories:
    PLANKS = MenuCategory(
        category=CreativeCategory.CONSTRUCTION, group="minecraft:itemGroup.name.planks"
    )
    WALLS = MenuCategory(
        category=CreativeCategory.CONSTRUCTION, group="minecraft:itemGroup.name.walls"
    )
    FENCE = MenuCategory(
        category=CreativeCategory.CONSTRUCTION, group="minecraft:itemGroup.name.fence"
    )
    FENCE_GATE = MenuCategory(
        category=CreativeCategory.CONSTRUCTION,
        group="minecraft:itemGroup.name.fenceGate",
    )
    STAIRS = MenuCategory(
        category=CreativeCategory.CONSTRUCTION, group="minecraft:itemGroup.name.stairs"
    )
    DOOR = MenuCategory(
        category=CreativeCategory.CONSTRUCTION, group="minecraft:itemGroup.name.door"
    )
    TRAPDOOR = MenuCategory(
        category=CreativeCategory.CONSTRUCTION,
        group="minecraft:itemGroup.name.trapdoor",
    )
    GLASS = MenuCategory(
        category=CreativeCategory.CONSTRUCTION, group="minecraft:itemGroup.name.glass"
    )
    GLASS_PANE = MenuCategory(
        category=CreativeCategory.CONSTRUCTION,
        group="minecraft:itemGroup.name.glassPane",
    )
    SLAB = MenuCategory(
        category=CreativeCategory.CONSTRUCTION, group="minecraft:itemGroup.name.slab"
    )
    STONE_BRICK = MenuCategory(
        category=CreativeCategory.CONSTRUCTION,
        group="minecraft:itemGroup.name.stoneBrick",
    )
    SANDSTONE = MenuCategory(
        category=CreativeCategory.CONSTRUCTION,
        group="minecraft:itemGroup.name.sandstone",
    )
    COPPER = MenuCategory(
        category=CreativeCategory.CONSTRUCTION, group="minecraft:itemGroup.name.copper"
    )
    WOOL = MenuCategory(
        category=CreativeCategory.CONSTRUCTION, group="minecraft:itemGroup.name.wool"
    )
    WOOL_CARPET = MenuCategory(
        category=CreativeCategory.CONSTRUCTION,
        group="minecraft:itemGroup.name.woolCarpet",
    )
    CONCRETE_POWDER = MenuCategory(
        category=CreativeCategory.CONSTRUCTION,
        group="minecraft:itemGroup.name.concretePowder",
    )
    CONCRETE = MenuCategory(
        category=CreativeCategory.CONSTRUCTION,
        group="minecraft:itemGroup.name.concrete",
    )
    STAINED_CLAY = MenuCategory(
        category=CreativeCategory.CONSTRUCTION,
        group="minecraft:itemGroup.name.stainedClay",
    )
    GLAZED_TERRACOTTA = MenuCategory(
        category=CreativeCategory.CONSTRUCTION,
        group="minecraft:itemGroup.name.glazedTerracotta",
    )

    HELMET = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.helmet"
    )
    CHESTPLATE = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.chestplate"
    )
    LEGGINGS = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.leggings"
    )
    BOOTS = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.boots"
    )
    SWORD = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.sword"
    )
    AXE = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.axe"
    )
    PICKAXE = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.pickaxe"
    )
    SHOVEL = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.shovel"
    )
    HOE = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.hoe"
    )
    ARROW = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.arrow"
    )
    COOKED_FOOD = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.cookedFood"
    )
    MISC_FOOD = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.miscFood"
    )
    HORSE_ARMOR = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.horseArmor"
    )
    POTION = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.potion"
    )
    SPLASH_POTION = MenuCategory(
        category=CreativeCategory.EQUIPMENT,
        group="minecraft:itemGroup.name.splashPotion",
    )
    LINGERING_POTION = MenuCategory(
        category=CreativeCategory.EQUIPMENT,
        group="minecraft:itemGroup.name.lingeringPotion",
    )
    BUNDLES = MenuCategory(
        category=CreativeCategory.EQUIPMENT, group="minecraft:itemGroup.name.bundles"
    )

    BED = MenuCategory(
        category=CreativeCategory.ITEMS, group="minecraft:itemGroup.name.bed"
    )
    ANVIL = MenuCategory(
        category=CreativeCategory.ITEMS, group="minecraft:itemGroup.name.anvil"
    )
    CHEST = MenuCategory(
        category=CreativeCategory.ITEMS, group="minecraft:itemGroup.name.chest"
    )
    SHULKER_BOX = MenuCategory(
        category=CreativeCategory.ITEMS, group="minecraft:itemGroup.name.shulkerBox"
    )
    RECORD = MenuCategory(
        category=CreativeCategory.ITEMS, group="minecraft:itemGroup.name.record"
    )
    SIGN = MenuCategory(
        category=CreativeCategory.ITEMS, group="minecraft:itemGroup.name.sign"
    )
    SKULL = MenuCategory(
        category=CreativeCategory.ITEMS, group="minecraft:itemGroup.name.skull"
    )
    BOAT = MenuCategory(
        category=CreativeCategory.ITEMS, group="minecraft:itemGroup.name.boat"
    )
    RAIL = MenuCategory(
        category=CreativeCategory.ITEMS, group="minecraft:itemGroup.name.rail"
    )
    MINECART = MenuCategory(
        category=CreativeCategory.ITEMS, group="minecraft:itemGroup.name.minecart"
    )
    BUTTONS = MenuCategory(
        category=CreativeCategory.ITEMS, group="minecraft:itemGroup.name.buttons"
    )
    PRESSURE_PLATE = MenuCategory(
        category=CreativeCategory.ITEMS, group="minecraft:itemGroup.name.pressurePlate"
    )
    BANNER_PATTERN = MenuCategory(
        category=CreativeCategory.ITEMS, group="minecraft:itemGroup.name.banner_pattern"
    )

    ORE = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.ore"
    )
    STONE = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.stone"
    )
    LOG = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.log"
    )
    WOOD = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.wood"
    )
    LEAVES = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.leaves"
    )
    SAPLING = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.sapling"
    )
    SEED = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.seed"
    )
    CROP = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.crop"
    )
    GRASS = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.grass"
    )
    CORAL_DECORATIONS = MenuCategory(
        category=CreativeCategory.NATURE,
        group="minecraft:itemGroup.name.coral_decorations",
    )
    FLOWER = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.flower"
    )
    DYE = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.dye"
    )
    RAW_FOOD = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.rawFood"
    )
    MUSHROOM = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.mushroom"
    )
    MONSTER_SPAWN_EGG = MenuCategory(
        category=CreativeCategory.NATURE,
        group="minecraft:itemGroup.name.monsterStoneEgg",
    )
    MOB_EGG = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.mobEgg"
    )
    CORAL = MenuCategory(
        category=CreativeCategory.NATURE, group="minecraft:itemGroup.name.coral"
    )


class BaseDescription(BaseModel):
    identifier: str
