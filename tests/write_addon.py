from mcaddon.ext.assetplus import *
from mcaddon import *

addon = Addon()
# with Addon.load('build/addon') as addon:

# BLOCK

blk = Block("test:block")
blk.add_component(OnFallOnComponent())
blk.add_component(OnInteractComponent())
blk.add_component(OnPlacedComponent())
blk.add_component(OnPlayerDestroyedComponent())
blk.add_component(OnPlayerPlacingComponent())
blk.add_component(OnStepOffComponent())
blk.add_component(OnStepOnComponent())
bv = BoneVisabilityComponent()
bv.add_bone("bone", Molang("false"))
blk.add_component(bv)
blk.add_component(BreathabilityComponent("air"))
blk.add_component(CollisionBoxComponent.cube())
blk.add_component(SelectionBoxComponent.cube())
ct = CraftingTableComponent("container.crafting_table")
ct.add_crafting_tag("crafting_table")
blk.add_component(ct)
blk.add_component(BlockDisplayNameComponent("tile.BLOCK.name"))
blk.add_component(DestructibleByExplosionComponent(0))
blk.add_component(DestructibleByMiningComponent(0))
blk.add_component(FlammableComponent())
blk.add_component(FrictionComponent(0.5))
blk.add_component(GeometryComponent("geometry.full_cube"))
blk.add_component(LightDampeningComponent(0))
blk.add_component(LightEmissionComponent(0))
blk.add_component(LootComponent(""))
blk.add_component(MapColorComponent("#f80"))
mi = MaterialInstancesComponent()
mi.add_material("*", Material("stone"))
blk.add_component(mi)
pf = PlacementFilterComponent()
blk.add_component(pf)
blk.add_component(QueuedTickingComponent([1, 1], Trigger("queued_ticking")))
blk.add_component(RandomTickingComponent(Trigger("random_ticking")))
blk.add_component(TransformationComponent.rotate(0, 0, 0))
blk.add_component(UnitCubeComponent())
bt = BlockTagsComponent()
bt.add_tag("stone")
blk.add_component(bt)
addon.add(blk)

# ITEM

itm = Item("test:item")
itm.add_component(IgnoresPermissionComponent(True))
itm.add_component(AllowOffHandComponent(True))
itm.add_component(BlockPlacerComponent("stone"))
itm.add_component(CanDestroyInCreativeComponent(True))
itm.add_component(CooldownComponent("", 1))
itm.add_component(DamageComponent(1))
itm.add_component(ItemDisplayNameComponent("item.ITEM"))
itm.add_component(DurabilityComponent(1, 1))
itm.add_component(EnchantableComponent("chestplate", 1))
itm.add_component(EntityPlacerComponent("armor_stand"))
itm.add_component(FoodComponent(1, 1))
itm.add_component(FuelComponent(1))
itm.add_component(GlintComponent(True))
itm.add_component(HandEquippedComponent(True))
itm.add_component(HoverTextColorComponent("red"))
itm.add_component(IconComponent("apple"))
itm.add_component(InteractButtonComponent("test"))
itm.add_component(ItemStorageComponent(1))
itm.add_component(LiquidClippedComponent(True))
itm.add_component(MaxStackSizeComponent(16))
itm.add_component(ProjectileComponent("arrow", 1))
itm.add_component(RecordComponent(1, 1, "cat"))
itm.add_component(RepairableComponent())
sc = ShooterComponent(True, 1, True)
sc.add_ammunition("arrow")
itm.add_component(sc)
itm.add_component(ShouldDespawnComponent(True))
itm.add_component(StackedByDataComponent(True))
itm.add_component(TagsComponent())
itm.add_component(ThrowableComponent(True, 1, 1, 1, 1, True))
itm.add_component(UseAnimationComponent(UseAnimation.eat))
itm.add_component(UseModifiersComponent(1, 1))
itm.add_component(WearableComponent(1, 1))
itm.add_component(DiggerComponent(True))
addon.add(itm)

# VOLUME

vol = Volume("test:volume")
vol.add_component(FogComponent("fog_savanna", 1))
vol.add_component(OnActorEnterComponent([Trigger("on_enter")]))
vol.add_component(OnActorLeaveComponent([Trigger("on_leave")]))
vol.add_event("on_enter", RunCommand("say on_enter"))
vol.add_event("on_leave", RunCommand("say on_leave"))
addon.add(vol)

addon.save("build/addon", zipped=False, overwrite=True)