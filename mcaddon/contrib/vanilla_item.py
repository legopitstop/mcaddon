__all__ = [
    "PICKAXE",
    "SHOVEL",
    "AXE",
    "SWORD",
    "BUNDLE",
    "SPEAR",
    "HOE",
]

from molang.dsl import MolangExpr, query
from mcaddon import (
    Item,
    MenuCategories,
    ItemIconComponent,
    ItemMaxStackSizeComponent,
    ItemDurabilityComponent,
    ItemDiggerComponent,
    ItemTagsComponent,
    ItemStorageItemComponent,
    ItemStorageWeightLimitComponent,
    ItemStorageWeightModifierComponent,
    ItemBundleInteractionComponent,
    ItemRepairableComponent,
    ItemEnchantableComponent,
    ItemHandEquippedComponent,
    ItemCooldownComponent,
    ItemUseModifiersComponent,
    ItemSwingDurationComponent,
    ItemSwingSoundsComponent,
    ItemDamageComponent,
    ItemPiercingWeaponComponent,
    ItemKineticWeaponComponent,
    ItemFuelComponent,
    KineticEffectConditions,
    DestroySpeed,
    BlockTags,
    ItemTags,
    RepairItem,
    EnchantableSlot,
    ItemCooldownType,
)

PICKAXE = Item()
PICKAXE.description.identifier = "mcaddon:wooden_pickaxe"
PICKAXE.description.menu_category = MenuCategories.PICKAXE
PICKAXE.components.add(ItemIconComponent().add("wooden_pickaxe"))
PICKAXE.components.add(ItemMaxStackSizeComponent(value=1))
PICKAXE.components.add(ItemDurabilityComponent(max_durability=4))
PICKAXE.components.add(
    ItemDiggerComponent().add(
        DestroySpeed(
            block=BlockTags(
                tags=query.any_tag("minecraft:is_pickaxe_item_destructible")
            ),
            speed=60,
        )
    )
)
PICKAXE.components.add(
    ItemRepairableComponent()
    .add(
        RepairItem(
            repair_amount=MolangExpr("context.other->query.remaining_durability")
        ).add("minecraft:wooden_pickaxe")
    )
    .add(
        RepairItem(repair_amount=query.max_durability * 0.25).add(
            ItemTags(tags=query.all_tags("minecraft:planks"))
        )
    )
)
PICKAXE.components.add(
    ItemTagsComponent(
        tags=[
            "minecraft:wooden_tier",
            "minecraft:is_pickaxe",
            "minecraft:is_tool",
        ]
    )
)
PICKAXE.components.add(ItemEnchantableComponent(slot=EnchantableSlot.PICKAXE, value=15))
PICKAXE.components.add(ItemHandEquippedComponent())
PICKAXE.components.add(ItemFuelComponent(duration=10))

SHOVEL = Item()
SHOVEL.description.identifier = "mcaddon:wooden_shovel"
SHOVEL.description.menu_category = MenuCategories.SHOVEL
SHOVEL.components.add(ItemIconComponent().add("wooden_shovel"))
SHOVEL.components.add(ItemMaxStackSizeComponent(value=1))
SHOVEL.components.add(ItemDurabilityComponent(max_durability=4))
SHOVEL.components.add(
    ItemDiggerComponent().add(
        DestroySpeed(
            block=BlockTags(
                tags=query.any_tag("minecraft:is_shovel_item_destructible")
            ),
            speed=60,
        )
    )
)
SHOVEL.components.add(
    ItemRepairableComponent()
    .add(
        RepairItem(
            repair_amount=MolangExpr("context.other->query.remaining_durability")
        ).add("minecraft:wooden_shovel")
    )
    .add(
        RepairItem(repair_amount=query.max_durability * 0.25).add(
            ItemTags(tags=query.all_tags("minecraft:planks"))
        )
    )
)
SHOVEL.components.add(
    ItemTagsComponent(
        tags=[
            "minecraft:wooden_tier",
            "minecraft:is_shovel",
            "minecraft:is_tool",
        ]
    )
)
SHOVEL.components.add(ItemEnchantableComponent(slot=EnchantableSlot.SHOVEL, value=15))
SHOVEL.components.add(ItemHandEquippedComponent())
SHOVEL.components.add(ItemFuelComponent(duration=10))

AXE = Item()
AXE.description.identifier = "mcaddon:wooden_axe"
AXE.description.menu_category = MenuCategories.AXE
AXE.components.add(ItemIconComponent().add("wooden_axe"))
AXE.components.add(ItemMaxStackSizeComponent(value=1))
AXE.components.add(ItemDurabilityComponent(max_durability=4))
AXE.components.add(
    ItemDiggerComponent().add(
        DestroySpeed(
            block=BlockTags(tags=query.any_tag("minecraft:is_axe_item_destructible")),
            speed=60,
        )
    )
)
AXE.components.add(
    ItemRepairableComponent()
    .add(
        RepairItem(
            repair_amount=MolangExpr("context.other->query.remaining_durability")
        ).add("minecraft:wooden_axe")
    )
    .add(
        RepairItem(repair_amount=query.max_durability * 0.25).add(
            ItemTags(tags=query.all_tags("minecraft:planks"))
        )
    )
)
AXE.components.add(
    ItemTagsComponent(
        tags=["minecraft:wooden_tier", "minecraft:is_axe", "minecraft:is_tool"]
    )
)
AXE.components.add(ItemEnchantableComponent(slot=EnchantableSlot.AXE, value=15))
AXE.components.add(ItemHandEquippedComponent())
AXE.components.add(ItemFuelComponent(duration=10))

SWORD = Item()
SWORD.description.identifier = "mcaddon:wooden_sword"
SWORD.description.menu_category = MenuCategories.SWORD
SWORD.components.add(ItemIconComponent().add("wooden_sword"))
SWORD.components.add(ItemMaxStackSizeComponent(value=1))
SWORD.components.add(ItemDurabilityComponent(max_durability=4))
SWORD.components.add(
    ItemDiggerComponent()
    .add(
        DestroySpeed(
            block=BlockTags(tags=query.any_tag("minecraft:is_sword_item_destructible")),
            speed=60,
        )
    )
    .add(
        DestroySpeed(
            block="minecraft:web",
            speed=60,
        )
    )
    .add(
        DestroySpeed(
            block="minecraft:bamboo",
            speed=60,
        )
    )
)
SWORD.components.add(
    ItemRepairableComponent()
    .add(
        RepairItem(
            repair_amount=MolangExpr("context.other->query.remaining_durability")
        ).add("minecraft:wooden_sword")
    )
    .add(
        RepairItem(repair_amount=query.max_durability * 0.25).add(
            ItemTags(tags=query.all_tags("minecraft:planks"))
        )
    )
)
SWORD.components.add(
    ItemTagsComponent(
        tags=[
            "minecraft:wooden_tier",
            "minecraft:is_sword",
            "minecraft:is_tool",
        ]
    )
)
SWORD.components.add(ItemEnchantableComponent(slot=EnchantableSlot.SWORD, value=15))
SWORD.components.add(ItemHandEquippedComponent())
SWORD.components.add(ItemDamageComponent(value=1))
SWORD.components.add(ItemFuelComponent(duration=10))

HOE = Item()
HOE.description.identifier = "mcaddon:wooden_hoe"
HOE.description.menu_category = MenuCategories.HOE
HOE.components.add(ItemIconComponent().add("wooden_hoe"))
HOE.components.add(ItemMaxStackSizeComponent(value=1))
HOE.components.add(ItemDurabilityComponent(max_durability=4))
HOE.components.add(
    ItemDiggerComponent().add(
        DestroySpeed(
            block=BlockTags(tags=query.any_tag("minecraft:is_hoe_item_destructible")),
            speed=60,
        )
    )
)
HOE.components.add(
    ItemRepairableComponent()
    .add(
        RepairItem(
            repair_amount=MolangExpr("context.other->query.remaining_durability")
        ).add("minecraft:wooden_hoe")
    )
    .add(
        RepairItem(repair_amount=query.max_durability * 0.25).add(
            ItemTags(tags=query.all_tags("minecraft:planks"))
        )
    )
)
HOE.components.add(
    ItemTagsComponent(
        tags=["minecraft:wooden_tier", "minecraft:is_hoe", "minecraft:is_tool"]
    )
)
HOE.components.add(ItemEnchantableComponent(slot=EnchantableSlot.HOE, value=15))
HOE.components.add(ItemHandEquippedComponent())
HOE.components.add(ItemFuelComponent(duration=10))

SPEAR = Item()
SPEAR.description.identifier = "mcaddon:wooden_spear"
SPEAR.components.add(ItemIconComponent().add("wood_spear"))
SPEAR.components.add(ItemMaxStackSizeComponent(value=1))
SPEAR.components.add(ItemDurabilityComponent(max_durability=60))
SPEAR.components.add(
    ItemRepairableComponent()
    .add(
        RepairItem(
            repair_amount=MolangExpr("context.other->query.remaining_durability")
        ).add("minecraft:wooden_spear")
    )
    .add(
        RepairItem(repair_amount=query.max_durability * 0.25).add(
            ItemTags(tags=query.all_tags("minecraft:planks"))
        )
    )
)
SPEAR.components.add(
    ItemTagsComponent().add("minecraft:wooden_tier", "minecraft:is_spear")
)
SPEAR.components.add(
    ItemEnchantableComponent(slot=EnchantableSlot.MELEE_SPEAR, value=15)
)
SPEAR.components.add(ItemHandEquippedComponent())
SPEAR.components.add(
    ItemUseModifiersComponent(
        use_duration=72000,
        emit_vibrations=True,
        start_sound="item.wooden_spear.use",
        movement_modifier=1.0,
    )
)
SPEAR.components.add(
    ItemCooldownComponent(category="spear", duration=0.65, type=ItemCooldownType.ATTACK)
)
SPEAR.components.add(ItemSwingDurationComponent(value=0.65))
SPEAR.components.add(
    ItemSwingSoundsComponent(
        attack_miss="item.wooden_spear.attack_miss",
        attack_hit="item.wooden_spear.attack_hit",
    )
)
SPEAR.components.add(ItemDamageComponent(value=1))
SPEAR.components.add(ItemFuelComponent(duration=10))
SPEAR.components.add(ItemPiercingWeaponComponent())
SPEAR.components.add(
    ItemKineticWeaponComponent(
        delay=15,
        damage_multiplier=0.7,
        damage_conditions=KineticEffectConditions(
            max_duration=300, min_relative_speed=4.6
        ),
        knockback_conditions=KineticEffectConditions(max_duration=200, min_speed=5.1),
        dismount_conditions=KineticEffectConditions(max_duration=100, min_speed=14.0),
    )
)

BUNDLE = Item()
BUNDLE.description.identifier = "mcaddon:wooden_bundle"
BUNDLE.description.menu_category = MenuCategories.BUNDLES
BUNDLE.components.add(
    ItemIconComponent()
    .add("bundle")
    .add("bundle_open_back", "bundle_open_back")
    .add("bundle_open_front", "bundle_open_front")
)
BUNDLE.components.add(ItemMaxStackSizeComponent(value=1))
BUNDLE.components.add(
    ItemStorageItemComponent(max_slots=64, allow_nested_storage_items=True).banned(
        "minecraft:shulker_box", "minecraft:undyed_shulker_box"
    )
)
BUNDLE.components.add(ItemStorageWeightLimitComponent(max_weight_limit=64))
BUNDLE.components.add(ItemStorageWeightModifierComponent(weight_in_storage_item=4))
BUNDLE.components.add(ItemBundleInteractionComponent(num_viewable_slots=12))
