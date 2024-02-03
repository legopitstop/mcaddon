from mcaddon import *

blk = Block("test:on_interact_change_state_block")
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
blk.add_component(QueuedTickingComponent([60, 60], Trigger("queued_ticking")))
blk.add_component(RandomTickingComponent(Trigger("random_ticking")))
blk.add_component(TransformationComponent.rotate(0, 0, 0))
blk.add_component(UnitCubeComponent())
bt = BlockTagsComponent()
bt.add_tag("stone")
blk.add_component(bt)

blk.add_event("on_fall_on", RunCommand("say on_fall_on"))
blk.add_event("on_interact", RunCommand("say on_interact"))
blk.add_event("on_placed", RunCommand("say on_placed"))
blk.add_event("on_player_destoryed", RunCommand("say on_player_destoryed"))
blk.add_event("on_player_placing", RunCommand("say on_player_placing"))
blk.add_event("on_step_off", RunCommand("say on_step_off"))
blk.add_event("on_step_on", RunCommand("say on_step_on"))
blk.add_event("queued_ticking", RunCommand("say queued_ticking"))
blk.add_event("random_ticking", RunCommand("say random_ticking"))

blk.save("build/")
